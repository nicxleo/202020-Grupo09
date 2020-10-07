package uniandes.rf1.mr;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class WCReducer extends Reducer<Text, IntWritable, Text, DoubleWritable> {

    @Override
    protected void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
        List<TripEntity> items = new ArrayList<>();
        for (IntWritable w : values) {
            TripEntity obj = items.stream().filter(x -> x.ZonaDesde == w.get()).findAny().orElse(null);
            if (obj == null) {
                obj = new TripEntity();
                obj.ZonaDesde = w.get();
                obj.Cantidad = 1;
                items.add(obj);
            } else {
                obj.Cantidad++;
            }
        }

        TripEntity max = Collections.max(items, Comparator.comparing(x -> x.Cantidad));

        context.write(new Text(key + "_" + max.ZonaDesde), new DoubleWritable(max.Cantidad));
    }
}
