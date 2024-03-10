import altair as alt

def return_ranking_chart(title, subtitle, data_input, metric_name, list_of_scale):
    data_input = data_input.rename(columns={metric_name: "metric"})

    ranking_viz = (
        alt.Chart(
            data_input,
            title=alt.Title(
                title,
                subtitle=subtitle,
            ),
        )
        .mark_bar(size=11, color="#4899F3")
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

    return (ranking_viz + ranking_text_viz).properties(width=180)
