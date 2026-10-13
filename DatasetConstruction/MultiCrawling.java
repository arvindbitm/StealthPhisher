import java.net.URI;
import java.net.http.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class MultiCrawling {
    String[] IDs;
    String[] URLs;
    int count = 0;

    public MultiCrawling() {
        readList();
        for (int i = 0; i < count; i++) {
            try {
                new Thread(new MultiDownload(IDs[i], URLs[i])).start();
                Thread.sleep(500);
            } catch (Exception e) {
                // Handle the exception
                System.err.println(IDs[i] + " - Error starting download thread: " + e);
            }
        }
    }

    void readList() {
        try {
            Path file = Paths.get("url.txt");
            count = (int) Files.lines(file).count();
            IDs = new String[count];
            URLs = new String[count];
            System.out.println("Total URLs: " + count);

            List<String> allLines = Files.readAllLines(file);
            int i = 0;
            for (String line : allLines) {
                int delimiterIndex = line.indexOf(" ");
                if (delimiterIndex == -1) {
                    // Handle lines without a space delimiter
                    System.err.println("Invalid line format in url.txt: " + line);
                    continue;
                }

                IDs[i] = line.substring(0, delimiterIndex);
                URLs[i] = line.substring(delimiterIndex + 1, line.length());
                // System.out.println(IDs[i] + "_" + URLs[i]);
                i++;
            }
        } catch (Exception e) {
            System.err.println("Error reading list: " + e);
        }
    }

    public static void main(String[] args) throws Exception {
        new MultiCrawling();
    }
}

class MultiDownload implements Runnable {
    String ID;
    String URL;

    MultiDownload(String id, String url) {
        ID = id;
        URL = url;
    }

    public void run() {
        try {
            String content = HttpClient.newHttpClient().send(HttpRequest.newBuilder().uri(URI.create(URL)).GET().build(), HttpResponse.BodyHandlers.ofString()).body();
            Files.writeString(Paths.get("D:\\Phishing\\WEBs\\" + ID + ".txt"), ID + " " + URL + "\n" + content, StandardCharsets.UTF_8);
            System.gc();
        } catch (Exception e) {
            System.err.println(ID + " - Crawl Error: " + e);
        }
    }
}
