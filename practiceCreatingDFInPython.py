import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

spark = SparkSession.builder.appName('edpresso').getOrCreate()

data = [("1234","Smith","John"),
    ("2222","Rose","Kale"),
    ("4331","Williams","Brain")
  ]

columns = ["StudentID","lastname","firstname"]
df = spark.createDataFrame(data = data, schema = columns)

df_with_ts = df.withColumn("curr_timestamp", current_timestamp())

df_with_ts.show(truncate=False)
