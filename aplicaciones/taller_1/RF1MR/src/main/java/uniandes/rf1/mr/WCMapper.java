package uniandes.rf1.mr;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.log4j.Logger;

public class WCMapper extends Mapper<LongWritable, Text, Text, IntWritable> {

    @Override
    protected void map(LongWritable key, Text value, Mapper.Context context) throws IOException, InterruptedException {

        Logger logger = Logger.getLogger(WCMapper.class);
        Configuration conf = context.getConfiguration();
        int pHoraDesde = Integer.parseInt(conf.get("HoraDesde"));
        int pHoraHasta = Integer.parseInt(conf.get("HoraHasta"));

        //logger.info("TRAZA PERSONALIZADA."+fileName);
        try {
            String[] vLstColumna = value.toString().split(",");
            IndexEntity index = Helper.GetIndex(vLstColumna);
            int vZonaDesde = Integer.parseInt(vLstColumna[index.ZonaDesde]);
            String vStringFechaDesde = vLstColumna[index.FechaDesde];
            Date vFechaDesde = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").parse(vStringFechaDesde);

            Calendar vCalendar = new GregorianCalendar();
            vCalendar.setTime(vFechaDesde);
            int hour = vCalendar.get(Calendar.HOUR_OF_DAY);
            
            if (hour >= pHoraDesde && hour <= pHoraHasta) {
                context.write(new Text("TipoVehiculo " + index.Tipo), new IntWritable(vZonaDesde));
            }
        } catch (Exception ex) {
        }
    }
}
