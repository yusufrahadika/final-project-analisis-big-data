package com.mind.naivebayesapps;

import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.res.Resources;
import android.os.Bundle;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.concurrent.TimeUnit;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {

    OkHttpClient client = new OkHttpClient();
    ProgressDialog progressDialog;

    Spinner[] spinners = new Spinner[6];
    Button btnSub;
    Button btnKelompok;

    private static final String url = "http://192.168.1.9:8000/api/naive";

    ArrayList<String[]> fitursVal = new ArrayList<>();
    String[] fiturs = new String[6];
    String mMessage;
    String hasilPredict;
    Double executionTime;
    Double postTime;

    private static final String TAG = "prediksi";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        spinners[0] = findViewById(R.id.fitur_1);
        spinners[1] = findViewById(R.id.fitur_2);
        spinners[2] = findViewById(R.id.fitur_3);
        spinners[3] = findViewById(R.id.fitur_4);
        spinners[4] = findViewById(R.id.fitur_5);
        spinners[5] = findViewById(R.id.fitur_6);

        Resources res = getResources();
        fitursVal.add(res.getStringArray(R.array.fitur_1_2_val));
        fitursVal.add(res.getStringArray(R.array.fitur_1_2_val));
        fitursVal.add(res.getStringArray(R.array.fitur_3_val));
        fitursVal.add(res.getStringArray(R.array.fitur_4_val));
        fitursVal.add(res.getStringArray(R.array.fitur_5_val));
        fitursVal.add(res.getStringArray(R.array.fitur_6_val));

        btnSub = findViewById(R.id.btnSubmit);
        btnKelompok = findViewById(R.id.btnKelompok);

        btnSub.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                boolean filled = true;
                for (Spinner sp : spinners) {
                    if (sp.getSelectedItemId() == 0L) {
                        filled = false;
                        break;
                    }
                }
                if (!filled) {
                    Toast.makeText(getApplicationContext(), "Lengkapi form terlebih dahulu", Toast.LENGTH_LONG).show();
                    return;
                }

                for (int i = 0; i < fiturs.length; i++) {
                    fiturs[i] = fitursVal.get(i)[(int) spinners[i].getSelectedItemId() - 1];
                }

                // progress dialog
                progressDialog = new ProgressDialog(view.getContext());
                progressDialog.setMessage("Loading..."); // Setting Message
                progressDialog.setProgressStyle(ProgressDialog.STYLE_SPINNER); // Progress Dialog Style Spinner
                progressDialog.show(); // Display Progress Dialog
                progressDialog.setCancelable(false);

                OkHttpClient.Builder builder = new OkHttpClient.Builder();
                builder.connectTimeout(5, TimeUnit.MINUTES) // connect timeout
                        .writeTimeout(5, TimeUnit.MINUTES) // write timeout
                        .readTimeout(5, TimeUnit.MINUTES); // read timeout

                client = builder.build();

                try {
                    postRequest();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });

        btnKelompok.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                alertDialogKelompok();
            }
        });
    }

    private void postRequest() throws IOException {
        MediaType MEDIA_TYPE = MediaType.parse("application/json");

        JSONObject postdata = new JSONObject();
        try {
            for (int i = 0; i < fiturs.length; i++) {
                Log.d("fiturs", fiturs[i]);
                postdata.put("fitur_" + (i + 1), fiturs[i]);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

        RequestBody body = RequestBody.create(MEDIA_TYPE, postdata.toString());

        Request request = new Request.Builder()
                .url(url)
                .post(body)
                .header("Accept", "application/json")
                .header("Content-Type", "application/json")
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                call.cancel();
                runOnUiThread(new Runnable() {
                    public void run() {
                        Toast.makeText(getApplicationContext(), "Koneksi gagal dilakukan", Toast.LENGTH_LONG).show();
                    }
                });

                // Dismiss the dialog
                progressDialog.dismiss();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                mMessage = response.body().string();
                System.out.println("ok");
                MainActivity.this.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        try {
                            //Dismiss the dialog
                            progressDialog.dismiss();

                            JSONObject json = new JSONObject(mMessage);
                            hasilPredict = json.getString("prediksi");
                            executionTime = json.getDouble("execution_time");
                            postTime = json.getDouble("post_time");
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                        alertDialog();
                    }
                });
                Log.e(TAG, mMessage);
            }
        });
    }

    private void alertDialog() {
        AlertDialog.Builder Peringatan = new AlertDialog.Builder(this);
        Peringatan.setTitle("Hasil Klasifikasi");
        Peringatan
                .setMessage(String.format("Hasil = %s\nWaktu eksekusi = %.2f\nWaktu post = %.2f", hasilPredict, executionTime, postTime))
                .setCancelable(false)
                .setPositiveButton("Ok", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface Peringatan, int id) {
                        Peringatan.dismiss();
                    }
                }).show();
    }

    private void alertDialogKelompok() {
        AlertDialog.Builder Peringatan = new AlertDialog.Builder(this);
        Peringatan.setTitle("All Teams");
        Peringatan
                .setMessage("1. Imam Cholissodin \n2. Diajeng Sekar Seruni \n3. Junda Alfiah Zulqornain \n4. Audi Nuermey Hanaf \n5. Afwan Ghofur \n6. Mikhael Alexander \n7. Muhammad Ismail Hasan \n8. Fadhil Yusuf Rahadika")
                .setCancelable(false)
                .setPositiveButton("Ok", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface Peringatan, int id) {
                        Peringatan.dismiss();
                    }
                }).show();
    }

}
