---
title: "Reading from Kafka in Bean streaming job with confluent schema registry"
last_modified_at: 2024-04-09
categories:
  - Beam
tags:
  - Kafka
  - Confluent Schema Registry
  - Java
  - Apache Beam
  - Streaming
  - GCP
  - 
---
# Reading from Kafka in Bean streaming job with confluent schema registry

We are using [Beam](https://beam.apache.org/) to do a streaming job of reading data from the topic and putting that in BigData tables for processing.  

![](/assets/images/streaming/apache-beam.png)

We are using [confluent Kafka](https://www.confluent.io/) and with kafka events we have multiple ways to put in messages, we could use a plain string format or a complex [Avro](https://avro.apache.org/) format

![](/assets/images/streaming/confluent-kafka.png)

When we developed initial version I went with string format and code for that is straight forward 

```Java
 PCollection<String> collection = Pipeline.apply("readFromKafka",KafkaIO.<String,String>read
                .withBootstrapServers("server")
                .withTopic("topicName")
                .withConsumerConfigUpdates(hashMap)
                .withKeyDeserializer(StringDeserializer.class)
                .withValueDeserializer(StringDeserializer.class)
                .commitOffsetsInFinalize()
                .withoutMetadata());
```

and when I started with a avro message, we had difficulty reading the message, I tried multiple ways of writing a customized Deserializer and even generated stubs for Avro schema tried to deserialize that to object form, and most of them failed with error of not having recognizing the schema.

When I searched internet, there were solutions described as below, but I was getting compilation errors because KafkaAvroDeserializer cannot be cast to a class extending Deserializer.

```Java
 PCollection<String> collection = Pipeline.apply("readFromKafka",KafkaIO.<String,String>read
                .withBootstrapServers("server")
                .withTopic("topicName")
                .withConsumerConfigUpdates(hashMap)
                .withKeyDeserializer(StringDeserializer.class)
                .withValueDeserializerAndCoder((Class)KafkaAvroDeserializer.class, AvroCoder.of(GenericRecord.class))
                .commitOffsetsInFinalize()
                .withoutMetadata());
```

upon investigating multiple options, finally found have to use a confluent schema registry and there is know simple way of reading the messages generically without need of custom deserializers or stubs.

Hope helps someone struck with similar problem

```Java
//in case your schema registry has authorization turned on (you should) have to provide credentials in the form of map

ConfluentSchemaRegistryDeserializerProvider provider = ConfluentSchemaRegistryDeserializerProvider.of("schema-registry-url",10,"subjectname",hashMap);


 PCollection<KV<String,GenericRecord>> collection = Pipeline.apply("readFromKafka",KafkaIO.<String,KV<String,GenericRecord>>read
                .withBootstrapServers("server")
                .withTopic("topicName")
                .withConsumerConfigUpdates(hashMap)
                .withKeyDeserializer(StringDeserializer.class)
                .withValueDeserializer(provider)
                .commitOffsetsInFinalize()
                .withoutMetadata());

```
I get the value as key value and GenericRecord.toString() can give you the json equivalent of the message.

Hope this helps someone who is looking forward to get messages generically from Confluent kafka Avro message with use of schema registry.

