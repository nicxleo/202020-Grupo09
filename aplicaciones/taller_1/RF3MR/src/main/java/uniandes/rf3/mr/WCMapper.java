package uniandes.rf3.mr;

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
        int pZonaHasta = Integer.parseInt(conf.get("ZonaHasta"));
        //logger.info("TRAZA PERSONALIZADA."+index.Tipo+"\t"+month+"\t"+vZonaDesde+"\t"+vZonaHasta);
        try {
            String[] vLstColumna = value.toString().split(",");
            IndexEntity index = Helper.GetIndex(vLstColumna);
            int vZonaDesde = Integer.parseInt(vLstColumna[index.ZonaDesde]);
            int vZonaHasta = Integer.parseInt(vLstColumna[index.ZonaHasta]);
            String vStringFechaDesde = vLstColumna[index.FechaDesde];
            Date vFechaDesde = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").parse(vStringFechaDesde);
            
            Calendar vCalendar = new GregorianCalendar();
            vCalendar.setTime(vFechaDesde);
            int hour = vCalendar.get(Calendar.HOUR_OF_DAY);
            int month = vCalendar.get(Calendar.MONTH) + 1;
            
            if (hour >= pHoraDesde && hour <= pHoraHasta && vZonaHasta == pZonaHasta) {
                context.write(new Text("Datos_" + month), new IntWritable(vZonaHasta));
            }
        } catch (Exception ex) {
        }
    }
}
