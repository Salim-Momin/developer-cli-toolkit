from rich.table import Table


def create_table(
    title: str | None = None,
    show_header: bool = True,
) -> Table:
    """Create a consistently styled DevKit table."""

    return Table(
        title=title,
        show_header=show_header,
        header_style="bold cyan",
        border_style="bright_black",
        row_styles=[
            "",
            "on black",
        ],
        padding=(0, 1),
    )

def create_key_value_table(
    title: str | None = None,
) -> Table:
    """Create a two-column DevKit information table."""

    table = create_table(
        title=title,
        show_header=False,
    )

    table.add_column(
        "Property",
        style="bold bright_black",
        no_wrap=True,
    )

    table.add_column(
        "Value",
    )

    return table