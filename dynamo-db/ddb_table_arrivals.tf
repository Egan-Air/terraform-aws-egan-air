resource "aws_dynamodb_table" "ArrivingFlights" {
  name           = "ArrivingFlights"
  billing_mode   = "PAY_PER_REQUEST"

  # Attribute definitions
  attribute {
    name = "arrival_time"
    type = "S"
  }
  attribute {
    name = "flight_id"
    type = "S"
  }

  # Key schema
  hash_key = "flight_id"
  range_key = "arrival_time"
}