import prepare_data
import classification
from pyspark.sql import SparkSession
import time
from pyspark.ml.feature import VectorAssembler
#import visualization
#import clustering

if __name__ == "__main__":

    start = time.time()
    spark = SparkSession.builder.appName("TSVD").getOrCreate()
    data = prepare_data.loadData(spark)
    data = data.sample(False, 0.2) #run Forrest run! 400s...
    #data, indexedData = prepare_data.preprocess(data, indexed=False)

    data, indexedData = prepare_data.preprocess(data)

    # tmp test
    indexedData.printSchema()
    data.printSchema()
    #prepare_data.number_to_text(data).show()

    # Visualization (sroti dlho)
    # data = prepare_data.preprocess(data, indexed=False)
    # visualization.make_barcharts(data, save_pdf=True)
    # visualization.make_histogram(data)

    # Clustering
    #clustering.kmeans_clustering(data)

    # feature vector prep
    col_names = indexedData.schema.names
    col_names.remove('Accident_Severity_Binary')
    print col_names
    vector_data = VectorAssembler(inputCols=col_names, outputCol="features").transform(indexedData)
    print vector_data

    training_data, testing_data = vector_data.randomSplit([0.8, 0.2], seed=1234)

    classification.decisionTree(training_data,testing_data)
    #classification.supportVectorMachine(training_data,testing_data)
    #classification.naiveBayes(training_data,testing_data)
    #classification.randomForrest(training_data,testing_data)
    #classification.gradientBoostedTrees(training_data,testing_data)

    end = time.time()
    print end - start

    spark.stop()


