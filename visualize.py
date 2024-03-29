""" This module contains the visualize/chart making part """

import altair as alt

WIDTH_VISUALIZATION = 500
BAR_COLOR = "#4899F3"

def get_ranking_chart(
        title,
        subtitle,
        data_input,
        metric_name,
        list_of_scale) -> alt.vegalite.v5.api.LayerChart:
    """
    This function creates a visualization using Altair library where
    countries in input data are sorted based on the performance
    at historical world cups.
        Parameters:
            title (String): A title for the visualization
            subtitle (String): A substitle for the visualization
            data_input (DataFrame): A DataFrame object for creating the visualization
            metric_name (String): The metric name used in the input DataFrame
            list_of_scale (List): List that contains a scale range
            for the visualization (lower limit, upper limit)
        Returns:
            (LayerChart) A chart created using altair library
    """

    data_input = data_input.rename(columns={metric_name: "metric"})

    # Creates the visual content
    ranking_viz = (
        alt.Chart(
            data_input,
            title=alt.Title(
                title,
                subtitle=subtitle,
            ),
        )
        .mark_bar(size=11, color=BAR_COLOR)
        .encode(
            x=alt.X(
                "metric:Q",
                axis=alt.Axis(ticks=False, labels=False),
                scale=alt.Scale(domain=list_of_scale),
            ).title(""),
            y=alt.Y(
                "country_name:N",
                axis=alt.Axis(ticks=False, labelPadding=10),
                sort=alt.EncodingSortField(field="metric", order="descending"),
            ).title(""),
            color=alt.Color("is_former_champion:N", legend=None),
        )
    )

    # Creates text component of the visualization
    ranking_text_viz = (
        alt.Chart(data_input)
        .mark_text(dx=10, align="left")
        .encode(
            x=alt.X("metric:Q", scale=alt.Scale(domain=list_of_scale)),
            y=alt.Y(
                "country_name:N",
                sort=alt.EncodingSortField(field="metric", order="descending"),
            ),
            text=alt.Text("metric:Q"),
        )
    )

    return (ranking_viz + ranking_text_viz).properties(width=WIDTH_VISUALIZATION)
