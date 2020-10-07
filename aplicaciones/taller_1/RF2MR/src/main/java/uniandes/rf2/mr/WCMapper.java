package uniandes.rf2.mr;

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
        int pZonaDesde = Integer.parseInt(conf.get("ZonaDesde"));
        int pZonaHasta = Integer.parseInt(conf.get("ZonaHasta"));
        int pMes = Integer.parseInt(conf.get("Mes"));
        //logger.info("TRAZA PERSONALIZADA."+pZonaDesde);
        try {
            String[] vLstColumna = value.toString().split(",");
            IndexEntity index = Helper.GetIndex(vLstColumna);
            int vZonaDesde = Integer.parseInt(vLstColumna[index.ZonaDesde]);
            int vZonaHasta = Integer.parseInt(vLstColumna[index.ZonaHasta]);
            String vStringFechaDesde = vLstColumna[index.FechaDesde];
            Date vFechaDesde = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").parse(vStringFechaDesde);

            Calendar vCalendar = new GregorianCalendar();
            vCalendar.setTime(vFechaDesde);
            int month = vCalendar.get(Calendar.MONTH) + 1;

            if (vZonaDesde == pZonaDesde && vZonaHasta == pZonaHasta && month == pMes) {
                Double vMontoTotal = Double.parseDouble(vLstColumna[index.MontoTotal]);
                context.write(new Text("Datos"), new DoubleWritable(vMontoTotal));
            }
        } catch (Exception ex) {
        }
    }
}
