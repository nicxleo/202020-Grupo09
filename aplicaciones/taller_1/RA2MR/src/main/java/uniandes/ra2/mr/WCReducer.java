package uniandes.ra2.mr;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class WCReducer extends Reducer<Text, DoubleWritable, Text, DoubleWritable> {

    @Override
    protected void reduce(Text key, Iterable<DoubleWritable> values, Context context) throws IOException, InterruptedException {
        List<Double> items = new ArrayList<>();
        for (DoubleWritable w : values) {
            items.add(w.get());
        }

        context.write(key, new DoubleWritable(items.size()));
    }
}
