package uniandes.ra1.mr;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.log4j.Logger;

public class WCMapper extends Mapper<LongWritable, Text, Text, DoubleWritable> {

    @Override
    protected void map(LongWritable key, Text value, Mapper.Context context) throws IOException, InterruptedException {

        Logger logger = Logger.getLogger(WCMapper.class);
        Configuration conf = context.getConfiguration();
        //logger.info("TRAZA PERSONALIZADA."+pZonaDe);
        try {
            String[] vLstColumna = value.toString().split(",");
            int vZonaDe = Integer.parseInt(vLstColumna[7]);
            int vZonaHasta = Integer.parseInt(vLstColumna[8]);
            String vStringFecha = vLstColumna[1];
            Date vFechaPickup = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").parse(vStringFecha);

            context.write(new Text(vZonaDe + "_" + vZonaHasta), new DoubleWritable(1.0));

        } catch (Exception ex) {
        }
    }
}
