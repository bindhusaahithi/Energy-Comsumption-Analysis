terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "raw" {
  bucket = "${var.project_name}-${var.environment}-raw"
}

resource "aws_s3_bucket" "curated" {
  bucket = "${var.project_name}-${var.environment}-curated"
}

resource "aws_glue_catalog_database" "analytics" {
  name = "${replace(var.project_name, "-", "_")}_${var.environment}"
}

resource "aws_athena_workgroup" "analytics" {
  name = "${var.project_name}-${var.environment}-wg"

  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = true
    result_configuration {
      output_location = "s3://${aws_s3_bucket.curated.bucket}/athena-results/"
    }
  }
}

