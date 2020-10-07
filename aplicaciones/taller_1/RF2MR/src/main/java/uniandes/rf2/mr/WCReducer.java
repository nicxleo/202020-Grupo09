package uniandes.rf2.mr;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
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

        double min = items.stream().min(Comparator.naturalOrder()).get();
        double max = items.stream().max(Comparator.naturalOrder()).get();
        double avg = items.stream().mapToDouble(val -> val).average().orElse(0.0);
        context.write(new Text("Minimo"), new DoubleWritable(min));
        context.write(new Text("Maximo"), new DoubleWritable(max));
        context.write(new Text("Promedio"), new DoubleWritable(avg));
    }
}
