package uniandes.rf2.mr;

import java.io.IOException;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;

/**
 *
 * @author Esteb
 */
public class JobMR {

    private static String Entrada;
    private static String Salida;
    private static String ZonaDe;
    private static String ZonaHasta;
    private static String Mes;

    public static void main(String[] args) {
        int vMinParams = 5;
        if (args.length < vMinParams) {
            System.out.println("La aplicación requiere de (" + vMinParams + ") parámetros.");
            System.exit(-1);
        }

        Entrada = args[0];
        Salida = args[1];
        ZonaDe = args[2];
        ZonaHasta = args[3];
        Mes = args[4];

        try {
            RunJob();
        } catch (Exception ex) {
            System.out.println(ex.toString());
        }
    }

    public static void RunJob() throws IOException, InterruptedException, ClassNotFoundException {
        Configuration conf = new Configuration();
        //////////////////////
        //Parameters
        //////////////////////
        conf.set("ZonaDe", ZonaDe);
        conf.set("ZonaHasta", ZonaHasta);
        conf.set("Mes", Mes);
        //////////////////////
        //Job
        //////////////////////
        Job wcJob = Job.getInstance(conf, "RF2 Job");
        wcJob.setJarByClass(JobMR.class);
        //////////////////////
        //Mapper
        //////////////////////
        wcJob.setMapperClass(WCMapper.class);
        wcJob.setMapOutputKeyClass(Text.class);
        wcJob.setMapOutputValueClass(DoubleWritable.class);
        ///////////////////////////
        //Reducer
        ///////////////////////////
        wcJob.setReducerClass(WCReducer.class);
        wcJob.setOutputKeyClass(Text.class);
        wcJob.setOutputValueClass(DoubleWritable.class);
        ///////////////////////////
        //Input Format
        ///////////////////////////
        TextInputFormat.setInputPaths(wcJob, new Path(Entrada));
        wcJob.setInputFormatClass(TextInputFormat.class);
        ////////////////////
        ///Output Format
        //////////////////////
        TextOutputFormat.setOutputPath(wcJob, new Path(Salida));
        wcJob.setOutputFormatClass(TextOutputFormat.class);
        wcJob.waitForCompletion(true);
        System.out.println(wcJob.toString());
    }
}
