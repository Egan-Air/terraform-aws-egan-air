resource "aws_dynamodb_table" "FlightSchedules" {
  name           = "FlightSchedules"
  billing_mode   = "PAY_PER_REQUEST"

  # Attribute definitions
  attribute {
    name = "departure_time"
    type = "S"
  }
  attribute {
    name = "flight_id"
    type = "S"
  }

  # Key schema
  hash_key = "flight_id"
  range_key = "departure_time"
}