package com.mind.naivebayesapps;

import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.os.Bundle;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity{

    OkHttpClient client = new OkHttpClient();
    ProgressDialog progressDialog;

    EditText fitur1, fitur2, fitur3;
    Button btnSub;
    Button btnKelompok;

    private static final String url = "http://54.204.185.51:8001/api/naive";

    String fitur_1, fitur_2, fitur_3;
    String mMessage;
    String hasilPredic;

    private static final String TAG = "prediksi";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        fitur1 = findViewById(R.id.fitur_1);
        fitur2 = findViewById(R.id.fitur_2);
        fitur3 = findViewById(R.id.fitur_3);

        btnSub= (Button) findViewById(R.id.btnSubmit);
        btnKelompok= (Button) findViewById(R.id.btnKelompok);

        btnSub.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                fitur_1 = fitur1.getText().toString();
                fitur_2 = fitur2.getText().toString();
                fitur_3 = fitur3.getText().toString();

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
            postdata.put("fitur_1", fitur_1);
            postdata.put("fitur_2", fitur_2);
            postdata.put("fitur_3", fitur_3);
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
                System.out.println("no");
                String mMessage = e.getMessage();
                // hasilPredic = mMessage.toString();
                // alertDialog();
                Log.w("failure Response", e);
//                call.cancel();

                //Dismiss the dialog
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
                            hasilPredic = json.getString("prediksi");
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
                .setMessage(hasilPredic)
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
                .setMessage("1. Imam Cholissodin \n2. Diajeng Sekar Seruni \n3. Junda Alfiah Zulqornain \n4. Audi Nuermey Hanaf \n5. Afwan Ghofur \n6. Mikhael Alexander \n7. Muhammad Ismail Hasan")
                .setCancelable(false)
                .setPositiveButton("Ok", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface Peringatan, int id) {
                        Peringatan.dismiss();
                    }
                }).show();
    }

}
