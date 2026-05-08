from flask import Flask, render_template, request, jsonify

# IMPORTANT: must be named "app" for Vercel detection
app = Flask(__name__)


# Normalize incoming measurements into millimetres
def morph_to_mm(raw_span, scale_tag):

    if scale_tag == "cm":
        return raw_span * 10

    elif scale_tag == "um":
        return raw_span / 1000

    return raw_span


# Convert millimetres into preferred output scale
def reshape_from_mm(base_span, target_tag):

    if target_tag == "cm":
        return base_span / 10

    elif target_tag == "um":
        return base_span * 1000

    return base_span


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def resolve_specimen_scale():

    payload = request.get_json()

    projected_span = float(payload["image_size"])
    zoom_factor = float(payload["magnification"])

    incoming_scale = payload["image_unit"]
    export_scale = payload["output_unit"]

    # Convert incoming measurement into mm
    normalized_span = morph_to_mm(
        projected_span,
        incoming_scale
    )

    # Core biology formula
    organism_span_mm = normalized_span / zoom_factor

    # Convert into selected output unit
    translated_span = reshape_from_mm(
        organism_span_mm,
        export_scale
    )

    return jsonify({
        "actual_size": round(translated_span, 4),
        "unit": export_scale
    })


# Only runs locally, ignored by Vercel/Render
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
