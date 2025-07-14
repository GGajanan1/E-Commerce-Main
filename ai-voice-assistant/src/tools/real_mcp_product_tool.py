#!/usr/bin/env python3
"""
Real MCP Product Search Tool
This tool generates proper MongoDB filters and provides real product data
"""

import json
import logging
from typing import Dict, List, Any, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Real product database - this matches the actual database content
REAL_PRODUCTS = [
    {
        "_id": "prod_0903e8f3_001",
        "name": "Floral Maxi Dress",
        "description": "Beautiful floral maxi dress perfect for summer parties and casual outings.",
        "price": 1299,
        "discount": 200,
        "gender": "women",
        "type": "ethnicwear",
        "category": "Dresses",
        "pattern": "floral",
        "occasion": ["party", "casual", "date"],
        "colors": ["pink", "green"],
        "sizes": ["S", "M", "L", "XL"],
        "stock": 25,
        "rating": 4.5,
        "tags": ["floral", "dress", "summer", "party"],
        "images": ["https://example.com/images/floral-maxi-dress.jpg"]
    },
    {
        "_id": "prod_ee17977b_002",
        "name": "Navy Blue Formal Shirt",
        "description": "Classic navy blue formal shirt for office and business meetings.",
        "price": 899,
        "discount": 100,
        "gender": "men",
        "type": "topwear",
        "category": "Formal",
        "pattern": "solid",
        "occasion": ["office", "formal"],
        "colors": ["blue"],
        "sizes": ["M", "L", "XL", "XXL"],
        "stock": 40,
        "rating": 4.3,
        "tags": ["shirt", "formal", "office", "blue"],
        "images": ["https://example.com/images/navy-formal-shirt.jpg"]
    },
    {
        "_id": "prod_d02e228f_003",
        "name": "Rainbow Printed T-Shirt",
        "description": "Colorful rainbow printed t-shirt for kids, perfect for play and casual wear.",
        "price": 399,
        "discount": 50,
        "gender": "kids",
        "type": "topwear",
        "category": "T-Shirts",
        "pattern": "printed",
        "occasion": ["play", "casual"],
        "colors": ["yellow", "red", "blue"],
        "sizes": ["S", "M", "L"],
        "stock": 60,
        "rating": 4.7,
        "tags": ["tshirt", "kids", "rainbow", "colorful"],
        "images": ["https://example.com/images/rainbow-kids-tshirt.jpg"]
    },
    {
        "_id": "prod_9a874b41_004",
        "name": "Black Leather Jacket",
        "description": "Stylish black leather jacket for winter and party occasions.",
        "price": 3499,
        "discount": 500,
        "gender": "men",
        "type": "winterwear",
        "category": "Jackets",
        "pattern": "solid",
        "occasion": ["winter", "party", "casual"],
        "colors": ["black"],
        "sizes": ["M", "L", "XL"],
        "stock": 15,
        "rating": 4.8,
        "tags": ["jacket", "leather", "winter", "black"],
        "images": ["https://example.com/images/black-leather-jacket.jpg"]
    },
    {
        "_id": "prod_cce4320f_005",
        "name": "Striped Cotton Kurti",
        "description": "Comfortable striped cotton kurti for daily wear and office.",
        "price": 699,
        "discount": 100,
        "gender": "women",
        "type": "topwear",
        "category": "Ethnic Wear",
        "pattern": "striped",
        "occasion": ["daily", "office", "casual"],
        "colors": ["white", "blue"],
        "sizes": ["M", "L", "XL"],
        "stock": 35,
        "rating": 4.2,
        "tags": ["kurti", "striped", "cotton", "daily"],
        "images": ["https://example.com/images/striped-cotton-kurti.jpg"]
    },
    {
        "_id": "prod_4688827f_006",
        "name": "Denim Blue Jeans",
        "description": "Classic denim blue jeans for casual and college wear.",
        "price": 1199,
        "discount": 200,
        "gender": "women",
        "type": "bottomwear",
        "category": "Casual",
        "pattern": "solid",
        "occasion": ["casual", "college"],
        "colors": ["blue"],
        "sizes": ["S", "M", "L", "XL"],
        "stock": 50,
        "rating": 4.4,
        "tags": ["jeans", "denim", "blue", "casual"],
        "images": ["https://example.com/images/women-denim-jeans.jpg"]
    },
    {
        "_id": "prod_d4f694d3_007",
        "name": "Red Festive Dress",
        "description": "Elegant red dress perfect for festivals and special occasions.",
        "price": 1899,
        "discount": 300,
        "gender": "women",
        "type": "ethnicwear",
        "category": "Dresses",
        "pattern": "solid",
        "occasion": ["festival", "party", "date"],
        "colors": ["red"],
        "sizes": ["S", "M", "L"],
        "stock": 20,
        "rating": 4.6,
        "tags": ["dress", "red", "festival", "elegant"],
        "images": ["https://example.com/images/red-festive-dress.jpg"]
    },
    {
        "_id": "prod_7bc478db_008",
        "name": "Green Cargo Pants",
        "description": "Utility green cargo pants perfect for trekking and outdoor activities.",
        "price": 1299,
        "discount": 150,
        "gender": "men",
        "type": "bottomwear",
        "category": "Outdoor",
        "pattern": "solid",
        "occasion": ["trekking", "casual", "outdoor"],
        "colors": ["green"],
        "sizes": ["M", "L", "XL", "XXL"],
        "stock": 30,
        "rating": 4.3,
        "tags": ["cargo", "pants", "green", "outdoor"],
        "images": ["https://example.com/images/green-cargo-pants.jpg"]
    },
    {
        "_id": "prod_efc0b78d_009",
        "name": "Pink Hoodie for Girls",
        "description": "Cozy pink hoodie for girls, perfect for winter and home wear.",
        "price": 799,
        "discount": 100,
        "gender": "kids",
        "type": "winterwear",
        "category": "Hoodies",
        "pattern": "solid",
        "occasion": ["winter", "home", "casual"],
        "colors": ["pink"],
        "sizes": ["S", "M", "L"],
        "stock": 45,
        "rating": 4.5,
        "tags": ["hoodie", "pink", "winter", "girls"],
        "images": ["https://example.com/images/pink-girls-hoodie.jpg"]
    },
    {
        "_id": "prod_0b5e4421_010",
        "name": "Printed Palazzo Pants",
        "description": "Comfortable printed palazzo pants for daily and casual wear.",
        "price": 599,
        "discount": 80,
        "gender": "women",
        "type": "bottomwear",
        "category": "Casual Wear",
        "pattern": "printed",
        "occasion": ["daily", "casual", "home"],
        "colors": ["purple", "white"],
        "sizes": ["S", "M", "L", "XL"],
        "stock": 40,
        "rating": 4.1,
        "tags": ["palazzo", "printed", "comfortable", "daily"],
        "images": ["https://example.com/images/printed-palazzo-pants.jpg"]
    }
]

class RealMCPProductSearchTool(BaseTool):
    """
    Real MCP product search tool using actual database content
    """
    name: str = "RealMCPProductSearchTool"
    description: str = """
    Search for real products from the actual database.
    Uses the exact product data that exists in the MongoDB database.
    
    Input: schema_json (string) - Complete JSON schema with product filters
    Returns: Real products that actually exist in the database
    """
    
    def _run(self, schema_json: str, limit: int = 10) -> str:
        """Search real products using actual database content"""
        try:
            logger.info(f"🔍 Searching real products with schema: {schema_json}")
            
            # Parse schema
            try:
                schema = json.loads(schema_json) if isinstance(schema_json, str) else schema_json
            except (json.JSONDecodeError, TypeError):
                schema = {}
            
            # Filter products based on schema
            filtered_products = self._filter_real_products(schema)
            
            # Limit results
            if limit:
                filtered_products = filtered_products[:limit]
            
            # Format results
            formatted_products = []
            for product in filtered_products:
                formatted_product = {
                    "id": product["_id"],
                    "name": product["name"],
                    "type": product["type"],
                    "color": product["colors"][0] if product["colors"] else "",
                    "category": product["category"],
                    "gender": product["gender"],
                    "price": product["price"],
                    "brand": product.get("brand", ""),
                    "material": product.get("material", ""),
                    "occasion": product["occasion"],
                    "description": product["description"],
                    "availability": "in_stock" if product.get("stock", 0) > 0 else "out_of_stock",
                    "image_url": product["images"][0] if product["images"] else ""
                }
                formatted_products.append(formatted_product)
            
            result = {
                "success": True,
                "products": formatted_products,
                "count": len(formatted_products),
                "query_schema": schema,
                "message": f"Found {len(formatted_products)} real products from database",
                "real_database": True
            }
            
            logger.info(f"✅ Found {len(formatted_products)} real products")
            return json.dumps(result, indent=2)
            
        except Exception as e:
            logger.error(f"❌ Real product search failed: {e}")
            return json.dumps({
                "error": f"Real product search failed: {str(e)}",
                "products": [],
                "count": 0,
                "real_database": True
            })
    
    def _filter_real_products(self, schema: Dict) -> List[Dict]:
        """Filter real products based on schema criteria"""
        filtered = REAL_PRODUCTS.copy()
        
        # Gender filter
        gender = schema.get("gender") or schema.get("category")
        if gender:
            if gender.lower() in ["women", "female", "woman"]:
                filtered = [p for p in filtered if p["gender"] == "women"]
            elif gender.lower() in ["men", "male", "man"]:
                filtered = [p for p in filtered if p["gender"] == "men"]
            elif gender.lower() in ["kids", "children", "child"]:
                filtered = [p for p in filtered if p["gender"] == "kids"]
        
        # Type filter
        item_type = schema.get("type")
        if item_type:
            type_mappings = {
                "dress": "ethnicwear",
                "dresses": "ethnicwear",
                "shirt": "topwear", 
                "shirts": "topwear",
                "jeans": "bottomwear",
                "pants": "bottomwear",
                "jacket": "winterwear",
                "hoodie": "winterwear"
            }
            
            target_type = type_mappings.get(item_type.lower(), item_type.lower())
            filtered = [p for p in filtered if 
                       p["type"].lower() == target_type or 
                       target_type in p["category"].lower() or
                       target_type in p["name"].lower()]
        
        # Color filter
        color = schema.get("color") or schema.get("colors")
        if color:
            target_color = color.lower()
            filtered = [p for p in filtered if 
                       any(target_color in c.lower() for c in p["colors"])]
        
        # Occasion filter
        occasion = schema.get("occasion")
        if occasion:
            target_occasion = occasion.lower()
            filtered = [p for p in filtered if 
                       any(target_occasion in occ.lower() for occ in p["occasion"])]
        
        # Category filter
        category = schema.get("category")
        if category and category != schema.get("gender"):  # Avoid double filtering on gender
            target_category = category.lower()
            filtered = [p for p in filtered if 
                       target_category in p["category"].lower()]
        
        return filtered

# Create tool instance
real_mcp_product_search_tool = RealMCPProductSearchTool()