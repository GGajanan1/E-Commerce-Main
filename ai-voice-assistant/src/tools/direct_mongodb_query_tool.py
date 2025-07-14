#!/usr/bin/env python3
"""
Direct MongoDB Query Tool
Takes JSON schema from intent analysis and uses it directly as MongoDB query filter
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
        "rating": 4.2,
        "tags": ["shirt", "formal", "blue", "office"],
        "images": ["https://example.com/images/navy-formal-shirt.jpg"]
    },
    {
        "_id": "prod_a4b8c7d2_003",
        "name": "Black Leather Jacket",
        "description": "Stylish black leather jacket for men, perfect for evening and casual outings.",
        "price": 2599,
        "discount": 300,
        "gender": "men",
        "type": "winterwear",
        "category": "Jackets",
        "pattern": "solid",
        "occasion": ["evening", "casual", "party"],
        "colors": ["black"],
        "sizes": ["M", "L", "XL", "XXL"],
        "stock": 15,
        "rating": 4.7,
        "tags": ["leather", "jacket", "black", "evening"],
        "images": ["https://example.com/images/black-leather-jacket.jpg"]
    },
    {
        "_id": "prod_f9e3a1b5_004",
        "name": "Red Cotton T-Shirt",
        "description": "Comfortable red cotton t-shirt for casual and daily wear.",
        "price": 499,
        "discount": 50,
        "gender": "men",
        "type": "topwear",
        "category": "T-Shirts",
        "pattern": "solid",
        "occasion": ["casual", "daily"],
        "colors": ["red"],
        "sizes": ["S", "M", "L", "XL"],
        "stock": 60,
        "rating": 4.1,
        "tags": ["tshirt", "red", "cotton", "casual"],
        "images": ["https://example.com/images/red-cotton-tshirt.jpg"]
    },
    {
        "_id": "prod_d5c2e8f7_005",
        "name": "Blue Denim Jeans",
        "description": "Classic blue denim jeans for men, suitable for casual and outdoor activities.",
        "price": 1499,
        "discount": 200,
        "gender": "men",
        "type": "bottomwear",
        "category": "Casual",
        "pattern": "solid",
        "occasion": ["casual", "outdoor"],
        "colors": ["blue"],
        "sizes": ["M", "L", "XL", "XXL"],
        "stock": 35,
        "rating": 4.4,
        "tags": ["jeans", "denim", "blue", "casual"],
        "images": ["https://example.com/images/blue-denim-jeans.jpg"]
    },
    {
        "_id": "prod_c7a9b4e1_006",
        "name": "White Summer Dress",
        "description": "Elegant white summer dress for women, perfect for beach and casual outings.",
        "price": 899,
        "discount": 100,
        "gender": "women",
        "type": "ethnicwear",
        "category": "Dresses",
        "pattern": "solid",
        "occasion": ["beach", "summer", "casual"],
        "colors": ["white"],
        "sizes": ["S", "M", "L", "XL"],
        "stock": 20,
        "rating": 4.3,
        "tags": ["dress", "white", "summer", "beach"],
        "images": ["https://example.com/images/white-summer-dress.jpg"]
    },
    {
        "_id": "prod_b8f4d6a3_007",
        "name": "Grey Wool Sweater",
        "description": "Warm grey wool sweater for winter and cold weather.",
        "price": 1799,
        "discount": 250,
        "gender": "women",
        "type": "winterwear",
        "category": "Hoodies",
        "pattern": "solid",
        "occasion": ["winter", "casual"],
        "colors": ["grey"],
        "sizes": ["S", "M", "L", "XL"],
        "stock": 18,
        "rating": 4.6,
        "tags": ["sweater", "grey", "wool", "winter"],
        "images": ["https://example.com/images/grey-wool-sweater.jpg"]
    },
    {
        "_id": "prod_a3e7f2c9_008",
        "name": "Green Cargo Pants",
        "description": "Durable green cargo pants for men, ideal for outdoor and trekking activities.",
        "price": 1199,
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


class DirectMongoDBQueryInput(BaseModel):
    """Input schema for direct MongoDB query"""
    schema_json: str = Field(..., description="JSON schema from intent analysis to use as MongoDB query filter")


class DirectMongoDBQueryTool(BaseTool):
    """
    Tool that takes JSON schema from intent analysis and uses it directly as MongoDB query filter
    """
    name: str = "Direct MongoDB Query Tool"
    description: str = (
        "Takes a JSON schema from intent analysis and uses it directly as a MongoDB query filter. "
        "Handles mapping of schema fields to MongoDB operators like $in for arrays, $lt/$gt for prices, "
        "and direct equality for simple fields."
    )
    args_schema: type[BaseModel] = DirectMongoDBQueryInput
    
    def _run(self, schema_json: str) -> str:
        """
        Execute direct MongoDB query using the schema JSON
        """
        try:
            # Parse the JSON schema
            if isinstance(schema_json, str):
                schema = json.loads(schema_json)
            else:
                schema = schema_json
            
            logger.info(f"🔍 Direct MongoDB Query Input: {schema}")
            
            # Build MongoDB query filter from schema
            mongo_filter = self._build_mongo_filter(schema)
            
            logger.info(f"🔍 MongoDB Filter: {mongo_filter}")
            
            # Execute query on our product database
            results = self._execute_query(mongo_filter)
            
            # Format results
            formatted_results = []
            for product in results:
                formatted_product = {
                    "id": product["_id"],
                    "name": product["name"],
                    "price": product["price"],
                    "discount": product.get("discount", 0),
                    "final_price": product["price"] - product.get("discount", 0),
                    "description": product["description"],
                    "colors": product["colors"],
                    "sizes": product["sizes"],
                    "rating": product["rating"],
                    "stock": product["stock"],
                    "category": product["category"],
                    "gender": product["gender"],
                    "occasion": product["occasion"],
                    "pattern": product["pattern"]
                }
                formatted_results.append(formatted_product)
            
            result = {
                "success": True,
                "products": formatted_results,
                "count": len(formatted_results),
                "mongo_filter": mongo_filter,
                "original_schema": schema,
                "message": f"Found {len(formatted_results)} products using direct MongoDB query"
            }
            
            logger.info(f"✅ Direct MongoDB Query Success: {len(formatted_results)} products found")
            return json.dumps(result, indent=2)
            
        except Exception as e:
            logger.error(f"❌ Direct MongoDB Query failed: {e}")
            return json.dumps({
                "error": f"Direct MongoDB query failed: {str(e)}",
                "products": [],
                "count": 0,
                "mongo_filter": {},
                "original_schema": {}
            })
    
    def _build_mongo_filter(self, schema: Dict) -> Dict:
        """
        Build MongoDB query filter from schema JSON
        Maps schema fields to appropriate MongoDB operators
        """
        mongo_filter = {}
        
        # Direct equality mappings
        direct_fields = ['gender', 'type', 'pattern']
        for field in direct_fields:
            if field in schema:
                value = schema[field]
                if isinstance(value, list) and len(value) == 1:
                    mongo_filter[field] = value[0]
                elif isinstance(value, list) and len(value) > 1:
                    mongo_filter[field] = {"$in": value}
                else:
                    mongo_filter[field] = value
        
        # Special handling for category - make it more flexible
        if 'category' in schema:
            category_value = schema['category']
            if isinstance(category_value, list):
                # For categories, we'll be more flexible in matching
                mongo_filter['category'] = {"$in": category_value}
            else:
                mongo_filter['category'] = category_value
        
        # Array field mappings (use $in operator)
        array_fields = ['colors', 'occasion', 'tags', 'sizes']
        for field in array_fields:
            if field in schema:
                value = schema[field]
                if isinstance(value, list):
                    # For arrays, we want to find documents where the field array contains any of the values
                    mongo_filter[field] = {"$in": value}
                else:
                    # Single value, find documents where field array contains this value
                    mongo_filter[field] = value
        
        # Special handling for color/colors mapping
        if 'color' in schema:
            color_value = schema['color']
            if isinstance(color_value, list):
                mongo_filter['colors'] = {"$in": color_value}
            else:
                mongo_filter['colors'] = color_value
        
        # Price range mapping
        if 'price' in schema:
            price_value = schema['price']
            if isinstance(price_value, dict):
                price_filter = {}
                if 'min' in price_value:
                    price_filter['$gte'] = price_value['min']
                if 'max' in price_value:
                    price_filter['$lte'] = price_value['max']
                if price_filter:
                    mongo_filter['price'] = price_filter
            elif isinstance(price_value, (int, float)):
                # Exact price match
                mongo_filter['price'] = price_value
        
        # Price range shortcuts
        if 'min_price' in schema:
            mongo_filter['price'] = mongo_filter.get('price', {})
            mongo_filter['price']['$gte'] = schema['min_price']
        
        if 'max_price' in schema:
            mongo_filter['price'] = mongo_filter.get('price', {})
            mongo_filter['price']['$lte'] = schema['max_price']
        
        # Rating filter
        if 'rating' in schema:
            rating_value = schema['rating']
            if isinstance(rating_value, dict):
                rating_filter = {}
                if 'min' in rating_value:
                    rating_filter['$gte'] = rating_value['min']
                if 'max' in rating_value:
                    rating_filter['$lte'] = rating_value['max']
                if rating_filter:
                    mongo_filter['rating'] = rating_filter
            elif isinstance(rating_value, (int, float)):
                mongo_filter['rating'] = {"$gte": rating_value}
        
        # Min rating shortcut
        if 'min_rating' in schema:
            mongo_filter['rating'] = {"$gte": schema['min_rating']}
        
        return mongo_filter
    
    def _execute_query(self, mongo_filter: Dict) -> List[Dict]:
        """
        Execute the MongoDB-style query on our product database
        This simulates MongoDB's find() operation
        """
        results = []
        
        for product in REAL_PRODUCTS:
            if self._matches_filter(product, mongo_filter):
                results.append(product)
        
        return results
    
    def _matches_filter(self, product: Dict, mongo_filter: Dict) -> bool:
        """
        Check if a product matches the MongoDB filter
        Simulates MongoDB's document matching logic with flexible category matching
        """
        for field, condition in mongo_filter.items():
            product_value = product.get(field)
            
            if product_value is None:
                return False
            
            # Handle MongoDB operators
            if isinstance(condition, dict):
                for operator, value in condition.items():
                    if operator == '$in':
                        # Special handling for category to be more flexible
                        if field == 'category':
                            if not self._flexible_category_match(product_value, value):
                                return False
                        else:
                            # Check if product field (array or single value) contains any of the values
                            if isinstance(product_value, list):
                                if not any(item in value for item in product_value):
                                    return False
                            else:
                                if product_value not in value:
                                    return False
                    elif operator == '$gte':
                        if product_value < value:
                            return False
                    elif operator == '$lte':
                        if product_value > value:
                            return False
                    elif operator == '$gt':
                        if product_value <= value:
                            return False
                    elif operator == '$lt':
                        if product_value >= value:
                            return False
            else:
                # Direct equality check
                if field == 'category':
                    # Use flexible category matching for direct equality too
                    if not self._flexible_category_match(product_value, [condition]):
                        return False
                elif isinstance(product_value, list):
                    # For array fields, check if the condition value is in the array
                    if condition not in product_value:
                        return False
                else:
                    # For single value fields, direct comparison
                    if product_value != condition:
                        return False
        
        return True
    
    def _flexible_category_match(self, product_category: str, search_categories: List[str]) -> bool:
        """
        Flexible category matching that considers related categories
        """
        # Direct match first
        if product_category in search_categories:
            return True
        
        # Category mappings for flexible matching
        category_mappings = {
            'T-Shirts': ['Formal', 'Casual', 'T-Shirts'],  # T-shirts can be formal or casual
            'Shirts': ['Formal', 'Casual', 'T-Shirts'],
            'Dresses': ['Dresses', 'Ethnic Wear', 'Casual'],
            'Jackets': ['Jackets', 'Winterwear', 'Casual'],
            'Pants': ['Casual', 'Formal', 'Outdoor'],
            'Jeans': ['Casual', 'Outdoor']
        }
        
        # Check if any of the search categories map to the product category
        for search_cat in search_categories:
            if search_cat in category_mappings:
                if product_category in category_mappings[search_cat]:
                    return True
        
        # Check reverse mapping - if product category maps to search categories
        if product_category in category_mappings:
            for search_cat in search_categories:
                if search_cat in category_mappings[product_category]:
                    return True
        
        return False


# Create tool instance
direct_mongodb_query_tool = DirectMongoDBQueryTool()
