async function computeSpecimenScale() {

    const projectedSpan =
        parseFloat(
            document.getElementById(
                "specimenProjection"
            ).value
        );

    const opticZoom =
        parseFloat(
            document.getElementById(
                "opticZoom"
            ).value
        );

    const projectionScale =
        document.getElementById(
            "projectionScale"
        ).value;

    const exportScale =
        document.getElementById(
            "exportScale"
        ).value;


    // Validation
    if (!projectedSpan || !opticZoom) {

        alert(
            "Please enter valid measurements."
        );

        return;
    }


    const relay = await fetch("/calculate", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            image_size: projectedSpan,

            magnification: opticZoom,

            image_unit: projectionScale,

            output_unit: exportScale
        })
    });


    const resolvedData = await relay.json();


    document.getElementById(
        "bioscopeResult"
    ).innerText =

        `${resolvedData.actual_size} ${resolvedData.unit}`;
}