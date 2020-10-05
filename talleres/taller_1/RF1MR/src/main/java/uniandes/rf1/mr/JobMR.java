package uniandes.rf1.mr;

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
    private static String HoraDesde;
    private static String HoraHasta;

    public static void main(String[] args) {
        int vMinParams = 4;
        if (args.length < vMinParams) {
            System.out.println("La aplicación requiere de (" + vMinParams + ") parámetros.");
            System.exit(-1);
        }

        Entrada = args[0];
        Salida = args[1];
        HoraDesde = args[2];
        HoraHasta = args[3];        

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
        conf.set("HoraDesde", HoraDesde);
        conf.set("HoraHasta", HoraHasta);
        //////////////////////
        //Job
        //////////////////////
        Job wcJob = Job.getInstance(conf, "RF1 Job");
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
