from google.cloud import bigquery
import os

# Initialize BigQuery client
client = bigquery.Client()

# Tool 1: Get product info
def get_product_info(product_name: str) -> list:
    """
    Fetch product details (all variants) from BigQuery
    based on product name.

    Args:
        product_name (str): Name of the product (e.g., "iPhone 17")

    Returns:
        list: List of product details (dict format)
    """

    query = """
    SELECT *
    FROM
        `track-1-project-491804.ecommerce_data.product_detail`
    WHERE
        LOWER(product_name) LIKE LOWER(@product_name)
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "product_name",
                "STRING",
                f"%{product_name}%"
            )
        ]
    )

    query_job = client.query(query, job_config=job_config)
    results = query_job.result()

    # Convert to list of dictionaries
    output = [dict(row) for row in results]

    return output



# Tool 2: Comparison
def compare_products(product_1: str, product_2: str) -> dict:
    """
    Compare two products based on specifications and price.

    Args:
        product_1 (str): First product name (e.g., "iPhone 17")
        product_2 (str): Second product name (e.g., "Samsung Galaxy S26")

    Returns:
        dict: Comparison data for both products
    """

    query = """
    SELECT *
    FROM
        `track-1-project-491804.ecommerce_data.product_detail`
    WHERE
        LOWER(product_name) LIKE LOWER(@product_1)
        OR LOWER(product_name) LIKE LOWER(@product_2)
    ORDER BY product_name, price
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                "product_1", "STRING", f"%{product_1}%"
            ),
            bigquery.ScalarQueryParameter(
                "product_2", "STRING", f"%{product_2}%"
            )
        ]
    )

    query_job = client.query(query, job_config=job_config)
    results = query_job.result()

    # Convert to structured format
    comparison = {
        product_1: [],
        product_2: []
    }

    for row in results:
        row_dict = dict(row)
        name = row_dict["product_name"]

        if product_1.lower() in name.lower():
            comparison[product_1].append(row_dict)
        elif product_2.lower() in name.lower():
            comparison[product_2].append(row_dict)

    return comparison


    