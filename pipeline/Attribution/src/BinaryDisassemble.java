import java.io.*;
import java.nio.file.Files;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Calendar;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.text.SimpleDateFormat;

import javax.script.ScriptException;



public class BinaryDisassemble {
	
	public static final String configPath = "config/binary_project.conf";
    	public static String test_dir;  
    	public static void readConfig(String fpath) throws IOException {
        	//ClassLoader classLoader = FeatureCalculators.class.getClass().getClassLoader();
	        File file = new File(fpath);
	        System.out.println(file.getAbsolutePath());
	        //System.out.println(classLoader.getResource(configPath));
	        BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(file)));
	        //BufferedReader reader = new BufferedReader(new InputStreamReader(classLoader.getResourceAsStream(configPath)));
	        String line = reader.readLine();
	        String parts[];
	        while(line != null) {
	                parts = line.split(" = ", 2);
	                switch(parts[0]) {
	                        case "testFolder":
	                                test_dir = parts[1];
	                                break;
	                        default:
	                                //System.err.println("Invalid option: " + parts[0]);
	                                break;
	                }
	                line = reader.readLine();
	        }
	        reader.close();
	    }
	public static void main(String[] args) throws FileNotFoundException, IOException, ClassNotFoundException, InterruptedException, ScriptException {
		try { readConfig(args[0]); } catch(ArrayIndexOutOfBoundsException ex) { readConfig(configPath); }   		
	      	List test_file_paths = Util.listCFiles(test_dir);
           	List test_binary_paths = Util.listBinaryFiles(test_dir);
           	List test_dis_paths = Util.listDisFiles(test_dir);
	         	           	
        	//delete all disassembled files
         	for(int bin=0; bin< test_dis_paths.size(); bin++){
        		System.out.println(test_dis_paths.get(bin).toString());
        			File toDelete = new File(test_dis_paths.get(bin).toString());
        			toDelete.delete();
        			}
           	
           	
          	//disassemble the binaries from the test folder 
           	for(int bin=0; bin< test_binary_paths.size(); bin++){
        		System.out.println(test_binary_paths.get(bin).toString());
        		if(!(new File(test_binary_paths.get(bin).toString() + ".dis").exists())){
        		disassembleBinaries(test_binary_paths.get(bin).toString(), "32");
        	//	stripBinaries(test_binary_paths.get(bin).toString());	
        		}
        			}
       	
   	}
     
		public static void disassembleBinaries(String filePath, String bits) throws IOException, InterruptedException, ScriptException{
			//should take filename to test each time
			//just needs the name of the directory with the authors and their source files as an input
		
			 Runtime disTime = Runtime.getRuntime();
			 String output_filename = filePath.concat(".dis");
			 String cmd1 = "ndisasm -b " +bits +" " + filePath.toString() + " > " + output_filename;      
		     Process disassemble = disTime.exec((new String[]{"/bin/sh","-c", cmd1}));
		     disassemble.waitFor();
		}

		public static void stripBinaries(String filePath) throws IOException, InterruptedException, ScriptException{
			
			 Runtime disTime = Runtime.getRuntime();
			 String output_filename = filePath;
			 String cmd1 = "strip -s " + filePath.toString() + " > " + output_filename;      
		     Process disassemble = disTime.exec((new String[]{"/bin/sh","-c", cmd1}));
		     disassemble.waitFor();
		}
				
	
}
	











