# analysis/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
import os
import re
from .utils import generate_summary_from_llm

# Load Excel data
DATA_FILE = os.path.join(os.path.dirname(__file__), '../real_estate_data.xlsx')
df = pd.read_excel(DATA_FILE)

class AnalyzeArea(APIView):
    def post(self, request):
        query = request.data.get('query', '').lower()
        
        # Clean the dataframe columns
        df.columns = df.columns.str.strip()
        
        # QUERY TYPE 1: Analyze a specific area
        if "analyze" in query:
            area = query.replace("analyze", "").strip().title()
            return self._analyze_area(area)
            
        # QUERY TYPE 2: Compare areas
        elif "compare" in query and "and" in query:
            areas = re.findall(r'compare\s+(.+?)\s+and\s+(.+?)(?:\s|$)', query)
            if areas:
                area1, area2 = areas[0][0].strip().title(), areas[0][1].strip().title()
                return self._compare_areas(area1, area2)
                
        # QUERY TYPE 3: Price growth for an area
        elif "price growth" in query or "growth" in query:
            match = re.search(r'(?:price growth|growth) for\s+(.+?)(?:\s+over|$)', query)
            if match:
                area = match.group(1).strip().title()
                years = 0
                if "over last" in query:
                    year_match = re.search(r'over last\s+(\d+)\s+years', query)
                    if year_match:
                        years = int(year_match.group(1))
                return self._price_growth(area, years)
                
        # QUERY TYPE 4: Show demand trends
        elif "demand trend" in query or "demand" in query:
            area = None
            if "for" in query:
                match = re.search(r'(?:demand trend|demand) for\s+(.+?)(?:\s|$)', query)
                if match:
                    area = match.group(1).strip().title()
            return self._demand_trends(area)
            
        # QUERY TYPE 5: General information about available data
        elif any(keyword in query for keyword in ["list", "show all", "available"]):
            if "areas" in query or "locations" in query:
                return self._list_areas()
            elif "years" in query:
                return self._list_years()
            elif "data" in query:
                return self._data_overview()
                
        # Default: Try to generate a response for any other query
        prompt = f"Answer this real estate data question: '{query}'. If you can't answer it specifically, suggest what kinds of queries would be better."
        summary = generate_summary_from_llm(prompt)
        
        return Response({
            "summary": summary,
            "chart": {"labels": [], "data": []},
            "table": []
        })
    
    def _analyze_area(self, area):
        area_df = df[df['final location'].str.strip().str.lower() == area.lower()]
        
        if area_df.empty:
            return Response({"summary": f"No data for {area}", "chart": {}, "table": []})
            
        # Group by year and average flat weighted rate
        chart_data = area_df.groupby("year")["flat - weighted average rate"].mean().reset_index()
        chart = {
            "labels": chart_data["year"].tolist(),
            "data": chart_data["flat - weighted average rate"].tolist()
        }
        
        # Generate LLM summary
        prompt = f"Give a short 2-3 line summary of real estate trends for {area} based on flat price and demand over the years. Mention key trends."
        summary = generate_summary_from_llm(prompt)
        
        return Response({
            "summary": summary,
            "chart": chart,
            "table": area_df.to_dict(orient='records')
        })
    
    def _compare_areas(self, area1, area2):
        area1_df = df[df['final location'].str.strip().str.lower() == area1.lower()]
        area2_df = df[df['final location'].str.strip().str.lower() == area2.lower()]
        
        if area1_df.empty or area2_df.empty:
            missing = []
            if area1_df.empty: missing.append(area1)
            if area2_df.empty: missing.append(area2)
            return Response({
                "summary": f"No data for {', '.join(missing)}",
                "chart": {},
                "table": []
            })
            
        # Create comparison chart data for flat prices
        area1_data = area1_df.groupby("year")["flat - weighted average rate"].mean().reset_index()
        area2_data = area2_df.groupby("year")["flat - weighted average rate"].mean().reset_index()
        
        # Merge on year
        combined = pd.merge(area1_data, area2_data, on="year", suffixes=('_area1', '_area2'))
        
        chart = {
            "labels": combined["year"].tolist(),
            "datasets": [
                {
                    "label": area1,
                    "data": combined["flat - weighted average rate_area1"].tolist()
                },
                {
                    "label": area2, 
                    "data": combined["flat - weighted average rate_area2"].tolist()
                }
            ]
        }
        
        # Create comparison table
        table_data = []
        for year in sorted(set(area1_df["year"].tolist() + area2_df["year"].tolist())):
            row = {"year": year}
            
            a1_data = area1_df[area1_df["year"] == year]
            a2_data = area2_df[area2_df["year"] == year]
            
            if not a1_data.empty:
                row[f"{area1} price"] = a1_data["flat - weighted average rate"].mean()
                row[f"{area1} sales"] = a1_data["flat_sold - igr"].sum()
            
            if not a2_data.empty:
                row[f"{area2} price"] = a2_data["flat - weighted average rate"].mean()
                row[f"{area2} sales"] = a2_data["flat_sold - igr"].sum()
                
            table_data.append(row)
        
        # Generate comparison summary
        prompt = f"Compare real estate trends between {area1} and {area2} in a 2-3 line summary. Focus on price differences and growth patterns."
        summary = generate_summary_from_llm(prompt)
        
        return Response({
            "summary": summary,
            "chart": chart,
            "table": table_data
        })
    
    def _price_growth(self, area, years=0):
        area_df = df[df['final location'].str.strip().str.lower() == area.lower()]
        
        if area_df.empty:
            return Response({"summary": f"No data for {area}", "chart": {}, "table": []})
        
        # Filter by years if specified
        if years > 0:
            max_year = area_df["year"].max()
            area_df = area_df[area_df["year"] >= max_year - years]
        
        # Calculate price growth data
        chart_data = area_df.groupby("year")["flat - weighted average rate"].mean().reset_index()
        
        if len(chart_data) <= 1:
            return Response({
                "summary": f"Insufficient data to calculate price growth for {area}",
                "chart": {},
                "table": []
            })
        
        # Calculate growth percentages
        chart_data["growth"] = chart_data["flat - weighted average rate"].pct_change() * 100
        chart_data["growth"] = chart_data["growth"].fillna(0)
        
        chart = {
            "labels": chart_data["year"].tolist(),
            "data": chart_data["growth"].tolist()
        }
        
        # Prepare table data with growth info
        table_data = []
        for i, row in chart_data.iterrows():
            table_data.append({
                "year": int(row["year"]),
                "price": row["flat - weighted average rate"],
                "growth_percentage": row["growth"]
            })
        
        # Calculate total and average growth
        first_price = chart_data.iloc[0]["flat - weighted average rate"]
        last_price = chart_data.iloc[-1]["flat - weighted average rate"]
        total_growth = ((last_price - first_price) / first_price) * 100
        avg_annual_growth = total_growth / (len(chart_data) - 1)
        
        prompt = f"Summarize price growth for {area} over the {'last ' + str(years) + ' years' if years > 0 else 'available period'}. Total growth is {total_growth:.2f}% with average annual growth of {avg_annual_growth:.2f}%."
        summary = generate_summary_from_llm(prompt)
        
        return Response({
            "summary": summary,
            "chart": chart,
            "table": table_data
        })
    
    def _demand_trends(self, area=None):
        if area:
            area_df = df[df['final location'].str.strip().str.lower() == area.lower()]
            if area_df.empty:
                return Response({"summary": f"No data for {area}", "chart": {}, "table": []})
                
            # Get sales data by year
            chart_data = area_df.groupby("year")[["flat_sold - igr", "shop_sold - igr", "office_sold - igr"]].sum().reset_index()
            
            chart = {
                "labels": chart_data["year"].tolist(),
                "datasets": [
                    {"label": "Flats Sold", "data": chart_data["flat_sold - igr"].tolist()},
                    {"label": "Shops Sold", "data": chart_data["shop_sold - igr"].tolist()},
                    {"label": "Offices Sold", "data": chart_data["office_sold - igr"].tolist()}
                ]
            }
            
            prompt = f"Analyze the demand trends for {area} based on sales data over time. How have flat, shop, and office sales changed?"
            summary = generate_summary_from_llm(prompt)
            
            return Response({
                "summary": summary,
                "chart": chart,
                "table": chart_data.to_dict(orient='records')
            })
        else:
            # Top 5 areas by demand/sales
            area_sales = df.groupby("final location")["flat_sold - igr"].sum().reset_index()
            top_areas = area_sales.sort_values("flat_sold - igr", ascending=False).head(5)
            
            chart = {
                "labels": top_areas["final location"].tolist(),
                "data": top_areas["flat_sold - igr"].tolist()
            }
            
            prompt = "Summarize the demand trends across different areas, highlighting the top areas by sales volume."
            summary = generate_summary_from_llm(prompt)
            
            return Response({
                "summary": summary,
                "chart": chart,
                "table": top_areas.to_dict(orient='records')
            })
    
    def _list_areas(self):
        areas = sorted(df["final location"].unique().tolist())
        
        return Response({
            "summary": f"There are {len(areas)} areas in the dataset. The complete list is shown in the table below.",
            "chart": {},
            "table": [{"area": area} for area in areas]
        })
    
    def _list_years(self):
        years = sorted(df["year"].unique().tolist())
        
        return Response({
            "summary": f"Data is available for the years {', '.join(map(str, years))}.",
            "chart": {},
            "table": [{"year": year} for year in years]
        })
    
    def _data_overview(self):
        overview = {
            "total_records": len(df),
            "years_covered": sorted(df["year"].unique().tolist()),
            "areas_count": len(df["final location"].unique()),
            "total_flats_sold": df["flat_sold - igr"].sum(),
            "average_flat_price": df["flat - weighted average rate"].mean()
        }
        
        prompt = f"Give an overview of the real estate dataset which has {overview['total_records']} records covering {len(overview['years_covered'])} years and {overview['areas_count']} areas."
        summary = generate_summary_from_llm(prompt)
        
        return Response({
            "summary": summary,
            "chart": {},
            "table": [overview]
        })
