package uniandes.ra2.mr;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.log4j.Logger;

public class WCMapper extends Mapper<LongWritable, Text, Text, DoubleWritable> {

    @Override
    protected void map(LongWritable key, Text value, Mapper.Context context) throws IOException, InterruptedException {

        Logger logger = Logger.getLogger(WCMapper.class);
        //logger.info("TRAZA PERSONALIZADA."+pZonaDe);
        try {
            String[] vLstColumna = value.toString().split(",");
            IndexEntity index = Helper.GetIndex(vLstColumna);
            String vStringFechaDesde = vLstColumna[index.FechaDesde];
            Date vFechaDesde = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").parse(vStringFechaDesde);

            Calendar vCalendar = new GregorianCalendar();
            vCalendar.setTime(vFechaDesde);
            int year = vCalendar.get(Calendar.YEAR);
            int month = vCalendar.get(Calendar.MONTH) + 1;
            int day = vCalendar.get(Calendar.DAY_OF_MONTH);

            if (day == 26 && month == 11) {
                context.write(new Text("AccionGracias_" + year), new DoubleWritable(1.0));
            }
            if (day == 19 && month == 9) {
                context.write(new Text("SanValentin_" + year), new DoubleWritable(1.0));
            }
            if (day == 25 && month == 12) {
                context.write(new Text("Navidad_" + year), new DoubleWritable(1.0));
            }
//            Date vFechaDesde = new SimpleDateFormat("dd-MM-yyyy").parse(pStringFechaDesde);
//            Date vFechaHasta = new SimpleDateFormat("dd-MM-yyyy").parse(pStringFechaHasta);
//
//            if (vFechaPickup.after(vFechaDesde) && vFechaPickup.before(vFechaHasta)) {
//                context.write(new Text("Datos"), new DoubleWritable(1.0));
//            }
        } catch (Exception ex) {
        }
    }
}
