
from flask import Blueprint, render_template, request
from models import Product

outfit_bp = Blueprint("outfit", __name__)


def score_outfit(top, bottom, jewellery):
    score = 40
    reasons = []

    # Compare colours.
    colours = {
        top.colour.lower(),
        bottom.colour.lower(),
        jewellery.colour.lower()
    }

    neutral_colours = {
        "black", "white", "beige", "cream", "grey",
        "gray", "gold", "silver", "brown", "navy"
    }

    if len(colours) == 1:
        score += 25
        reasons.append("The pieces share a coordinated colour.")
    elif any(colour in neutral_colours for colour in colours):
        score += 18
        reasons.append("Neutral colours help the outfit look coordinated.")
    else:
        score += 8
        reasons.append("The colours create a contrasting look.")

    # Compare styles.
    styles = [
        top.style_tag.lower(),
        bottom.style_tag.lower(),
        jewellery.style_tag.lower()
    ]

    if len(set(styles)) == 1:
        score += 25
        reasons.append("All three pieces share the same style.")
    elif len(set(styles)) == 2:
        score += 15
        reasons.append("Most pieces have a compatible style.")
    else:
        score += 5
        reasons.append("The pieces have different styles.")

    # Compare occasions.
    occasions = [
        top.occasion.lower(),
        bottom.occasion.lower(),
        jewellery.occasion.lower()
    ]

    if len(set(occasions)) == 1:
        score += 10
        reasons.append("All pieces suit the same occasion.")
    elif len(set(occasions)) == 2:
        score += 6
        reasons.append("The pieces are suitable for similar occasions.")
    else:
        score += 2
        reasons.append("Consider choosing pieces for the same occasion.")

    score = min(score, 100)

    if score >= 80:
        verdict = "Great Match"
    elif score >= 60:
        verdict = "Okay Match"
    else:
        verdict = "Try Another Combination"

    return score, verdict, " ".join(reasons)


@outfit_bp.route("/outfit", methods=["GET", "POST"])
def outfit():
    tops = Product.query.filter(
        Product.subcategory.ilike("%top%")
    ).all()

    bottoms = Product.query.filter(
        Product.subcategory.ilike("%bottom%")
    ).all()

    jewellery_items = Product.query.filter(
        Product.category == "Jewellery"
    ).all()

    result = None

    if request.method == "POST":
        top_id = request.form.get("top_id", type=int)
        bottom_id = request.form.get("bottom_id", type=int)
        jewellery_id = request.form.get("jewellery_id", type=int)

        top = Product.query.get(top_id) if top_id else None
        bottom = Product.query.get(bottom_id) if bottom_id else None
        jewellery = (
            Product.query.get(jewellery_id)
            if jewellery_id else None
        )

        valid_selection = (
            top is not None
            and bottom is not None
            and jewellery is not None
            and top.category != "Jewellery"
            and bottom.category != "Jewellery"
            and jewellery.category == "Jewellery"
        )

        if valid_selection:
            score, verdict, reason = score_outfit(
                top, bottom, jewellery
            )

            result = {
                "top": top,
                "bottom": bottom,
                "jewellery": jewellery,
                "score": score,
                "verdict": verdict,
                "reason": reason
            }
        else:
            result = {
                "error": (
                    "Please select a valid top, bottom, "
                    "and jewellery item."
                )
            }

    return render_template(
        "outfit.html",
        tops=tops,
        bottoms=bottoms,
        jewellery=jewellery_items,
        result=result
    )
