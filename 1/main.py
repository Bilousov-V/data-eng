import pyspark.sql as psql
from pyspark.sql.functions import split, array_join, lower, regexp_replace, slice, array

def main():
    path = "10K.github.jsonl"
    spark = psql.SparkSession.builder.getOrCreate()
    data = spark.read.json(path)
    m = data.filter(data.type == "PushEvent") \
        .select(data.payload.commits['author'][0]['name'].alias("Author"),
                data.payload.commits['message'][0].alias("Message")) \
        .filter(data.payload.commits['message'][0] != "NULL") 
    m = m.withColumn("Message", lower(array_join(slice(split(regexp_replace(m.Message, r'\n', ''), r' '), 1, 5), ' ')))
    m.withColumns({"Message":array_join(slice(split(m.Message, r' '), 1, 3), ' '),
                    ".":array_join(slice(split(m.Message, r' '), 2, 3), ' '),
                    "":array_join(slice(split(m.Message, r' '), 3, 3), ' ')}) \
     .coalesce(1).write.csv("data", mode="overwrite")
        
    spark.stop()
    pass

if __name__ == "__main__":
    main()
