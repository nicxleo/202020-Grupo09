package uniandes.mapRed;

import java.io.IOException;
import java.util.HashMap;


import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class WCMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
	
	@Override
	protected void map(LongWritable key, Text value,
			Context context)
			throws IOException, InterruptedException {
		String[] palabras = value.toString().split("([().,!?:;'\"-]|\\s)+");
		
		if (palabras.length > 100)
			context.write(new Text("Noticia Con más de 100 palabras"),new IntWritable(1));		
	}
}
