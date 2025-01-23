import json

def convert_dynamodb_to_terraform(input_file, output_file):
    with open(input_file, 'r') as infile:
        table_data = json.load(infile)

    table = table_data['Table']
    table_name = table['TableName']
    billing_mode = 'PROVISIONED' if 'ProvisionedThroughput' in table else 'PAY_PER_REQUEST'

    terraform_output = []

    terraform_output.append(f'resource "aws_dynamodb_table" "{table_name}" {{')
    terraform_output.append(f'  name           = "{table_name}"')
    terraform_output.append(f'  billing_mode   = "{billing_mode}"')

    if billing_mode == 'PROVISIONED':
        terraform_output.append('  provisioned_throughput {')
        terraform_output.append(f'    read_capacity  = {table["ProvisionedThroughput"]["ReadCapacityUnits"]}')
        terraform_output.append(f'    write_capacity = {table["ProvisionedThroughput"]["WriteCapacityUnits"]}')
        terraform_output.append('  }')

    # Attributes
    terraform_output.append('')
    terraform_output.append('  # Attribute definitions')
    for attribute in table['AttributeDefinitions']:
        terraform_output.append('  attribute {')
        terraform_output.append(f'    name = "{attribute["AttributeName"]}"')
        terraform_output.append(f'    type = "{attribute["AttributeType"]}"')
        terraform_output.append('  }')

    # Key Schema
    terraform_output.append('')
    terraform_output.append('  # Key schema')
    for key in table['KeySchema']:
        if key['KeyType'] == 'HASH':
            terraform_output.append(f'  hash_key = "{key["AttributeName"]}"')
        elif key['KeyType'] == 'RANGE':
            terraform_output.append(f'  range_key = "{key["AttributeName"]}"')

    # Global Secondary Indexes
    if 'GlobalSecondaryIndexes' in table:
        terraform_output.append('')
        terraform_output.append('  # Global Secondary Indexes')
        for gsi in table['GlobalSecondaryIndexes']:
            terraform_output.append('  global_secondary_index {')
            terraform_output.append(f'    name            = "{gsi["IndexName"]}"')
            terraform_output.append(f'    hash_key        = "{gsi["KeySchema"][0]["AttributeName"]}"')
            
            if len(gsi['KeySchema']) > 1:
                terraform_output.append(f'    range_key       = "{gsi["KeySchema"][1]["AttributeName"]}"')

            terraform_output.append(f'    projection_type = "{gsi["Projection"]["ProjectionType"]}"')
            
            if gsi['Projection']['ProjectionType'] == 'INCLUDE':
                terraform_output.append('    non_key_attributes = [')
                terraform_output.append(', '.join(f'"{attr}"' for attr in gsi['Projection']['NonKeyAttributes']))
                terraform_output.append('    ]')

            if 'ProvisionedThroughput' in gsi:
                terraform_output.append('    provisioned_throughput {')
                terraform_output.append(f'      read_capacity  = {gsi["ProvisionedThroughput"]["ReadCapacityUnits"]}')
                terraform_output.append(f'      write_capacity = {gsi["ProvisionedThroughput"]["WriteCapacityUnits"]}')
                terraform_output.append('    }')

            terraform_output.append('  }')

    # Tags
    if 'Tags' in table:
        terraform_output.append('')
        terraform_output.append('  # Tags')
        terraform_output.append('  tags = {')
        for tag in table['Tags']:
            terraform_output.append(f'    {tag["Key"]} = "{tag["Value"]}"')
        terraform_output.append('  }')

    terraform_output.append('}')

    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(terraform_output))

    print(f'Terraform configuration written to {output_file}')

# Example usage
# Replace 'table-details.json' with your input JSON file and 'dynamodb_table.tf' with your desired output file
convert_dynamodb_to_terraform('dyn-db-table-flight-sched.jsoon', 'ddb_table_flight_sched.tf')
