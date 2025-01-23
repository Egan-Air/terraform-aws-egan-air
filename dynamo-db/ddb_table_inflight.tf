resource "aws_dynamodb_table" "InFlight" {
  name           = "InFlight"
  billing_mode   = "PAY_PER_REQUEST"

  # Attribute definitions
  attribute {
    name = "flight_id"
    type = "S"
  }

  # Key schema
  hash_key = "flight_id"
}