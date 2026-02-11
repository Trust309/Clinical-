"""
Listing Optimization Agent

Handles listing quality and visibility:
- Title and description optimization
- SEO keyword analysis
- Amenity highlighting
- Competitive listing analysis
- Photo recommendations
- Review response generation
- Listing score evaluation
"""

from dataclasses import dataclass, field
from typing import Optional

from ..models.property import Property


HIGH_VALUE_AMENITIES = [
    "WiFi", "Air conditioning", "Heating", "Kitchen", "Washer", "Dryer",
    "Free parking", "Pool", "Hot tub", "Gym", "EV charger",
    "Self check-in", "Workspace", "TV", "Coffee maker",
    "Dishwasher", "Patio", "BBQ grill", "Fire pit", "Pet friendly",
    "Crib", "High chair", "Security cameras", "Smoke alarm",
    "Carbon monoxide alarm", "First aid kit", "Fire extinguisher",
]

PHOTO_CATEGORIES = [
    "exterior_front", "living_room", "kitchen", "primary_bedroom",
    "bathroom", "dining_area", "outdoor_space", "view",
    "amenity_highlights", "neighborhood",
]

SEO_KEYWORDS = {
    "location": [
        "downtown", "near beach", "mountain view", "city center",
        "quiet neighborhood", "walkable", "near airport",
    ],
    "features": [
        "modern", "spacious", "cozy", "luxury", "stylish", "renovated",
        "fully equipped", "designer", "bright", "charming",
    ],
    "experience": [
        "family friendly", "romantic getaway", "business travel",
        "vacation retreat", "weekend escape", "remote work",
        "group stay", "pet friendly",
    ],
    "unique": [
        "unique", "one of a kind", "award winning", "superhost",
        "newly listed", "hidden gem", "stunning views",
    ],
}


@dataclass
class ListingScore:
    """Evaluation of a listing's quality and completeness."""
    title_score: float = 0.0
    description_score: float = 0.0
    amenities_score: float = 0.0
    photos_score: float = 0.0
    pricing_score: float = 0.0
    response_rate_score: float = 0.0
    overall_score: float = 0.0
    recommendations: list[str] = field(default_factory=list)


class ListingOptimizationAgent:
    """Agent responsible for optimizing Airbnb listings."""

    def __init__(self):
        self.listing_scores: dict[str, ListingScore] = {}
        self.competitor_listings: list[dict] = []

    def generate_title(self, property: Property, style: str = "descriptive") -> list[str]:
        """Generate optimized listing title suggestions."""
        titles = []
        bedrooms = property.bedrooms
        ptype = property.property_type.value.replace("_", " ").title()

        adjectives = ["Charming", "Stylish", "Modern", "Cozy", "Spacious", "Beautiful"]

        # Extract location hint from address
        location = property.address.split(",")[-2].strip() if "," in property.address else ""

        if style == "descriptive":
            titles = [
                f"{adjectives[0]} {bedrooms}BR {ptype} in {location}" if location else f"{adjectives[0]} {bedrooms}BR {ptype}",
                f"{adjectives[1]} {ptype} | {bedrooms} Bed | {', '.join(property.amenities[:3])}" if property.amenities else f"{adjectives[1]} {bedrooms}BR {ptype}",
                f"{adjectives[2]} {bedrooms}-Bedroom Retreat" + (f" in {location}" if location else ""),
            ]
        elif style == "minimal":
            titles = [
                f"The {location} {ptype}" if location else f"The {ptype}",
                f"{bedrooms}BR · {property.max_guests} Guests" + (f" · {location}" if location else ""),
                f"{location} Hideaway" if location else f"Quiet {ptype} Retreat",
            ]
        elif style == "luxury":
            titles = [
                f"Luxury {bedrooms}BR {ptype}" + (f" | {location}" if location else ""),
                f"Designer {ptype} with Premium Amenities",
                f"Exclusive {bedrooms}-Bedroom" + (f" in {location}" if location else " Retreat"),
            ]

        # Ensure titles are under 50 characters (Airbnb recommendation)
        return [t[:50] for t in titles]

    def generate_description(self, property: Property) -> str:
        """Generate an optimized listing description."""
        amenities_text = ", ".join(property.amenities[:8]) if property.amenities else "all the essentials"

        description = f"""Welcome to {property.name}!

THE SPACE
This {property.property_type.value.replace('_', ' ')} features {property.bedrooms} bedroom(s) and {property.bathrooms} bathroom(s), comfortably accommodating up to {property.max_guests} guests. The space is thoughtfully designed to make you feel right at home.

AMENITIES
Enjoy {amenities_text}, and more. Everything you need for a comfortable stay is provided.

GETTING AROUND
{property.parking_info or 'Convenient access to local transportation and attractions.'}

HOUSE RULES
Please review our house rules to ensure a pleasant stay for everyone:
"""
        if property.house_rules:
            for rule in property.house_rules:
                description += f"• {rule}\n"
        else:
            description += "• Please treat the space with care\n• Quiet hours after 10 PM\n"

        description += f"""
CHECK-IN / CHECK-OUT
Check-in: {property.check_in_time}
Check-out: {property.check_out_time}

We're always available if you need anything during your stay. We look forward to hosting you!"""

        return description

    def evaluate_listing(
        self,
        property: Property,
        current_title: str = "",
        current_description: str = "",
        num_photos: int = 0,
        response_rate: float = 100.0,
        avg_review_score: float = 0.0,
    ) -> ListingScore:
        """Evaluate listing quality and provide a score with recommendations."""
        score = ListingScore()
        recommendations = []

        # Title evaluation
        title = current_title or property.name
        score.title_score = self._score_title(title)
        if score.title_score < 70:
            recommendations.append(
                "Improve your title: Include location, property type, and a compelling adjective. "
                "Keep it under 50 characters."
            )

        # Description evaluation
        score.description_score = self._score_description(current_description)
        if score.description_score < 70:
            recommendations.append(
                "Enhance your description: Add sections for The Space, Amenities, and Getting Around. "
                "Use bullet points and be specific about what makes your place special."
            )

        # Amenities evaluation
        score.amenities_score = self._score_amenities(property.amenities)
        missing = self._get_missing_amenities(property.amenities)
        if missing:
            recommendations.append(
                f"Consider adding these high-value amenities: {', '.join(missing[:5])}."
            )

        # Photos evaluation
        score.photos_score = min(100, (num_photos / 20) * 100)
        if num_photos < 10:
            recommendations.append(
                f"Add more photos. You have {num_photos}, but listings with 20+ photos perform better. "
                f"Cover: {', '.join(PHOTO_CATEGORIES[:5])}."
            )

        # Pricing evaluation (basic - without competitor data)
        score.pricing_score = 70  # Default without data

        # Response rate evaluation
        score.response_rate_score = response_rate
        if response_rate < 90:
            recommendations.append(
                "Improve your response rate. Aim for 90%+ to earn Superhost status. "
                "Consider using automated messages for common questions."
            )

        # Calculate overall score
        weights = {
            "title": 0.10,
            "description": 0.15,
            "amenities": 0.20,
            "photos": 0.25,
            "pricing": 0.15,
            "response_rate": 0.15,
        }
        score.overall_score = round(
            score.title_score * weights["title"]
            + score.description_score * weights["description"]
            + score.amenities_score * weights["amenities"]
            + score.photos_score * weights["photos"]
            + score.pricing_score * weights["pricing"]
            + score.response_rate_score * weights["response_rate"],
            1,
        )

        score.recommendations = recommendations
        self.listing_scores[property.property_id] = score
        return score

    def generate_review_response(
        self, guest_name: str, rating: int, review_text: str = ""
    ) -> str:
        """Generate a professional response to a guest review."""
        if rating >= 4:
            return (
                f"Thank you so much for the wonderful review, {guest_name}! "
                f"We're thrilled you enjoyed your stay. "
                f"We'd love to host you again anytime. Safe travels!"
            )
        elif rating == 3:
            return (
                f"Thank you for your feedback, {guest_name}. "
                f"We appreciate you taking the time to share your experience. "
                f"We're always working to improve, and your input helps us do that. "
                f"We hope to have the chance to provide a better experience next time."
            )
        else:
            return (
                f"Thank you for your honest feedback, {guest_name}. "
                f"We're sorry your experience didn't meet expectations. "
                f"We take all feedback seriously and are addressing the concerns you raised. "
                f"We'd welcome the opportunity to make things right."
            )

    def suggest_seo_keywords(self, property: Property) -> dict:
        """Suggest SEO keywords for the listing."""
        suggested = {}

        for category, keywords in SEO_KEYWORDS.items():
            relevant = []
            for kw in keywords:
                # Simple relevance matching based on property attributes
                if category == "features":
                    if property.bedrooms >= 3 and kw == "spacious":
                        relevant.append(kw)
                    elif property.bedrooms <= 1 and kw == "cozy":
                        relevant.append(kw)
                    else:
                        relevant.append(kw)  # Include all as suggestions
                elif category == "experience":
                    if property.max_guests >= 6 and kw == "group stay":
                        relevant.append(kw)
                    elif property.bedrooms >= 2 and kw == "family friendly":
                        relevant.append(kw)
                    else:
                        relevant.append(kw)
                else:
                    relevant.append(kw)

            suggested[category] = relevant[:5]

        return suggested

    def compare_with_competitors(
        self, property: Property, competitors: list[dict]
    ) -> dict:
        """Analyze listing against competitor listings."""
        if not competitors:
            return {"analysis": "No competitor data available."}

        avg_price = sum(c.get("price", 0) for c in competitors) / len(competitors)
        avg_rating = sum(c.get("rating", 0) for c in competitors) / len(competitors)
        avg_reviews = sum(c.get("num_reviews", 0) for c in competitors) / len(competitors)

        my_amenities = set(a.lower() for a in property.amenities)
        common_amenities = set()
        for c in competitors:
            for a in c.get("amenities", []):
                common_amenities.add(a.lower())

        missing_common = common_amenities - my_amenities
        unique_to_me = my_amenities - common_amenities

        return {
            "num_competitors": len(competitors),
            "avg_competitor_price": round(avg_price, 2),
            "my_price": property.base_price,
            "price_position": "above" if property.base_price > avg_price else "below",
            "avg_competitor_rating": round(avg_rating, 1),
            "avg_competitor_reviews": round(avg_reviews, 0),
            "amenities_competitors_have_i_dont": list(missing_common)[:10],
            "my_unique_amenities": list(unique_to_me),
            "recommendations": self._generate_competitive_recommendations(
                property, avg_price, avg_rating, missing_common
            ),
        }

    def get_photo_recommendations(self, property: Property, existing_photos: list[str] = None) -> dict:
        """Recommend photos to add or improve."""
        existing = set(existing_photos or [])
        missing = [cat for cat in PHOTO_CATEGORIES if cat not in existing]

        tips = {
            "exterior_front": "Shoot during golden hour. Show the full facade with good lighting.",
            "living_room": "Wide-angle shot showing the full room. Stage with pillows and throws.",
            "kitchen": "Clean countertops, add a bowl of fruit. Show all appliances.",
            "primary_bedroom": "Fresh linens, symmetrical pillows. Natural light preferred.",
            "bathroom": "Fresh towels, clean surfaces. Show shower and vanity.",
            "dining_area": "Set the table. Include chairs pushed in neatly.",
            "outdoor_space": "Show any patio, balcony, or garden. Include furniture.",
            "view": "Capture the best view from the property. Wide angle.",
            "amenity_highlights": "Close-ups of standout amenities (pool, hot tub, etc.).",
            "neighborhood": "Nearby attractions, restaurants, scenic spots.",
        }

        return {
            "missing_categories": missing,
            "tips": {cat: tips[cat] for cat in missing if cat in tips},
            "total_recommended": max(20, len(PHOTO_CATEGORIES)),
            "priority_shots": missing[:5] if missing else [],
        }

    def _score_title(self, title: str) -> float:
        """Score a listing title (0-100)."""
        score = 50.0
        if len(title) >= 10:
            score += 10
        if len(title) <= 50:
            score += 10
        if any(char.isdigit() for char in title):
            score += 10  # Includes bedroom count, etc.
        if any(kw in title.lower() for kws in SEO_KEYWORDS.values() for kw in kws):
            score += 20
        return min(score, 100)

    def _score_description(self, description: str) -> float:
        """Score a listing description (0-100)."""
        if not description:
            return 20.0
        score = 30.0
        if len(description) >= 200:
            score += 15
        if len(description) >= 500:
            score += 10
        sections = ["space", "amenit", "check-in", "getting around", "house rule"]
        for section in sections:
            if section in description.lower():
                score += 10
        return min(score, 100)

    def _score_amenities(self, amenities: list) -> float:
        """Score amenities completeness (0-100)."""
        if not amenities:
            return 10.0
        matched = sum(
            1 for a in amenities
            if any(hv.lower() in a.lower() for hv in HIGH_VALUE_AMENITIES)
        )
        return min(100, (matched / 10) * 100)

    def _get_missing_amenities(self, current: list) -> list[str]:
        """Identify high-value amenities not currently listed."""
        current_lower = set(a.lower() for a in current)
        return [
            a for a in HIGH_VALUE_AMENITIES
            if a.lower() not in current_lower
        ]

    def _generate_competitive_recommendations(
        self, property: Property, avg_price: float, avg_rating: float, missing_amenities: set
    ) -> list[str]:
        """Generate recommendations based on competitive analysis."""
        recs = []
        price_diff = ((property.base_price - avg_price) / avg_price) * 100 if avg_price else 0

        if price_diff > 20:
            recs.append(
                f"Your price is {price_diff:.0f}% above average. "
                "Ensure your amenities and quality justify the premium."
            )
        elif price_diff < -20:
            recs.append(
                f"Your price is {abs(price_diff):.0f}% below average. "
                "You may be able to increase your rate."
            )

        if missing_amenities:
            top_missing = list(missing_amenities)[:3]
            recs.append(
                f"Competitors commonly offer: {', '.join(top_missing)}. "
                "Consider adding these to stay competitive."
            )

        return recs
