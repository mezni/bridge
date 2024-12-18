
def get_unicode_chars(metric_graphic):
    if metric_graphic and metric_graphic=="arrows":
        return {
            "down_char":"UNICHAR(9660)",
            "steady_char":"UNICHAR(9679)",
            "up_char":"UNICHAR(9650)"
        }
    elif metric_graphic and metric_graphic=="traffic_lights":
        return {
            "down_char":"UNICHAR(128308)",
            "steady_char":"UNICHAR(128993)",
            "up_char":"UNICHAR(128994)"
        }

def get_mesure_result(metric_type):
    if metric_type == "value":
        result = "_result1 - _result2"
    elif metric_type == "percentage":
        result = "DIVIDE(_result1 - _result2, _result1, 0)"
    elif metric_type == "status":
        result = "IF(_result1 - _result2 < 0, -1, IF(_result1 - _result2 > 0, 1, 0))"
    else:
        result=None
    return result

def get_mesure_expression(metric_format,metric_graphic):
    if metric_format:
        if metric_graphic:
            expression = f"""IF(_result < 0, _down_char, IF(_result > 0, _up_char, _steady_char )) &" "& FORMAT(ABS(_result),"{metric_format}")"""
        else:
            expression = f"""FORMAT(_result,"{metric_format}")"""
    else:
        expression = f"""_result"""
    return expression

def generate_pop(config, output_file):
    default_date_table_name = "dimCalendrier"
    default_date_column_name = "Date"

    period = config.get("period", "Year")
    offset = config.get("offset", 1)
    table_name = config.get("table_name")
    column_name = config.get("column_name")
    date_table_name = config.get("date_table_name", default_date_table_name)
    date_column_name = config.get("date_column_name", default_date_column_name) 
    metrics = config.get("metrics", [{"type": "value"}]) 
    table_name_capt = table_name.capitalize() if table_name else "Table"

    if period == "Year":
        start_date = "IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 4, 1), DATE(YEAR(TODAY()) - 1, 4, 1))"
        end_date = "IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()) + 1, 3, 31), DATE(YEAR(TODAY()), 3, 31))"
        over_start_date = f"DATE(YEAR(_start_date) - {offset}, MONTH(_start_date), DAY(_start_date))"
        over_end_date = f"DATE(YEAR(_end_date) - {offset}, MONTH(_end_date), DAY(_end_date))"
        prefix = "YoY"
    elif period == "Month":
        start_date = "DATE(YEAR(TODAY()), MONTH(TODAY()), 1)"
        end_date = "EOMONTH(TODAY(), 0)"
        over_start_date = f"EDATE(_start_date, -{offset})"
        over_end_date = f"EDATE(_end_date, -{offset})"
        prefix = "MoM"
    else:
        print("Unsupported period.")
        return

    with open(output_file, 'a') as file:
        for metric in metrics:
            metric_type = metric.get("type")  
            metric_graphic = metric.get("graphic") 
            metric_format = metric.get("format") 
            if metric_graphic:
                unicode_chars = get_unicode_chars(metric_graphic)
                down_char = unicode_chars["down_char"]
                steady_char = unicode_chars["steady_char"]
                up_char = unicode_chars["up_char"]

            result=get_mesure_result(metric_type)
            expression=get_mesure_expression(metric_format,metric_graphic)

            graphics = """ """
            if metric_graphic:
                graphics = f""" 
    VAR _down_char = {down_char}
    VAR _steady_char = {steady_char}
    VAR _up_char = {up_char}"""

            template = f"""{graphics}
    VAR _start_date = {start_date}
    VAR _end_date = {end_date}
    VAR _over_start_date = {over_start_date}
    VAR _over_end_date = {over_end_date}
    VAR _result1 = CALCULATE(
        SUM({table_name}[{column_name}]),
        {date_table_name}[{date_column_name}] >= _start_date &&
        {date_table_name}[{date_column_name}] <= _end_date
    )
    VAR _result2 = CALCULATE(
        SUM({table_name}[{column_name}]),
        {date_table_name}[{date_column_name}] >= _over_start_date &&
        {date_table_name}[{date_column_name}] <= _over_end_date
    )
    VAR _result = {result}
    RETURN
        {expression}"""

            # Construct the measure name
            metric_initial = metric_type.upper()[:1]
            if metric_graphic:
                graphic_flag="G"
            if metric_format:
                format_flag="F"     
            name = f"{prefix}{table_name_capt}{period}{offset}{metric_initial}{graphic_flag}{format_flag}"

            # Write the generated measure to the file
            file.write(f"{name} = {template}\n\n")


def generate_gap(config, output_file):
    default_date_table_name = "dimCalendrier"
    default_date_column_name = "Date"

    period = config.get("period", "Year")
    src_table_name = config.get("src_table_name")
    src_column_name = config.get("src_column_name")
    dst_table_name = config.get("dst_table_name")
    dst_column_name = config.get("dst_column_name")
    date_table_name = config.get("date_table_name", default_date_table_name)
    date_column_name = config.get("date_column_name", default_date_column_name) 
    metrics = config.get("metrics", [{"type": "value"}]) 
    src_table_name_capt = src_table_name.capitalize() 
    dst_table_name_capt = dst_table_name.capitalize() 

    if period == "Year":
        start_date = "IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()), 4, 1), DATE(YEAR(TODAY()) - 1, 4, 1))"
        end_date = "IF(MONTH(TODAY()) >= 4, DATE(YEAR(TODAY()) + 1, 3, 31), DATE(YEAR(TODAY()), 3, 31))"
        prefix = "GoPY"
    elif period == "Month":
        start_date = "DATE(YEAR(TODAY()), MONTH(TODAY()), 1)"
        end_date = "EOMONTH(TODAY(), 0)"
        prefix = "GoPM"
    else:
        print("Unsupported period.")
        return

    with open(output_file, 'a') as file:
        for metric in metrics:
            metric_type = metric.get("type")  
            metric_graphic = metric.get("graphic") 
            metric_format = metric.get("format") 
            if metric_graphic:
                unicode_chars = get_unicode_chars(metric_graphic)
                down_char = unicode_chars["down_char"]
                steady_char = unicode_chars["steady_char"]
                up_char = unicode_chars["up_char"]

            result=get_mesure_result(metric_type)
            expression=get_mesure_expression(metric_format,metric_graphic)

            graphics = """ """
            if metric_graphic:
                graphics = f""" 
    VAR _down_char = {down_char}
    VAR _steady_char = {steady_char}
    VAR _up_char = {up_char}"""

            template = f"""{graphics}
    VAR _start_date = {start_date}
    VAR _end_date = {end_date}
    VAR _result1 = CALCULATE(
        SUM({src_table_name}[{src_column_name}]),
        {date_table_name}[{date_column_name}] >= _start_date &&
        {date_table_name}[{date_column_name}] <= _end_date
    )
    VAR _result2 = CALCULATE(
        SUM({dst_table_name}[{dst_column_name}]),
        {date_table_name}[{date_column_name}] >= _start_date &&
        {date_table_name}[{date_column_name}] <= _end_date
    )
    VAR _result = {result}
    RETURN
        {expression}"""

            # Construct the measure name
            metric_initial = metric_type.upper()[:1]
            if metric_graphic:
                graphic_flag="G"
            if metric_format:
                format_flag="F"     
            name = f"{prefix}{src_table_name_capt}{dst_table_name_capt}{period}{metric_initial}{graphic_flag}{format_flag}"

            # Write the generated measure to the file
            file.write(f"{name} = {template}\n\n")

configs = [
    {
    "type": "POP",
    "period": "Year",
    "offset": 1,
    "table_name": "reel",
    "column_name": "reel",
    "metrics": [{"type": "value", "format": "### ### ### $", "graphic": "arrows"},{"type": "percentage","format": "0 %", "graphic": "arrows"},{"type": "status"}]
    },
    {
    "type": "POP",
    "period": "Month",
    "offset": 1,
    "table_name": "reel",
    "column_name": "reel",
    "metrics": [{"type": "value", "format": "### ### ### $", "graphic": "arrows"},{"type": "percentage","format": "0 %", "graphic": "arrows"},{"type": "status"}]
    },
    {
    "type": "GAP",
    "period": "Month",
    "src_table_name": "reel",
    "src_column_name": "reel",
    "dst_table_name": "budget_prevision",
    "dst_column_name": "budget",
    "metrics": [{"type": "value", "format": "### ### ### $", "graphic": "arrows"},{"type": "percentage","format": "0 %", "graphic": "arrows"},{"type": "status"}]
    },
]

output_file="dax_measures.txt"
with open(output_file, 'w') as file:
    file.write(f"")
for config in configs:
    if config.get("type") == "POP":
        generate_pop(config, output_file)
    if config.get("type") == "GAP":
        generate_gap(config, output_file)