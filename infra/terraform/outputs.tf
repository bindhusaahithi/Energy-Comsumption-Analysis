output "raw_bucket_name" {
  value = aws_s3_bucket.raw.bucket
}

output "curated_bucket_name" {
  value = aws_s3_bucket.curated.bucket
}

output "glue_database_name" {
  value = aws_glue_catalog_database.analytics.name
}

