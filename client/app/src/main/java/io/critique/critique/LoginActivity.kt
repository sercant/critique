package io.critique.critique

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.view.View
import android.widget.Toast
import com.github.kittinunf.fuel.httpGet
import com.github.kittinunf.result.Result
import com.google.firebase.auth.FirebaseAuth
import io.critique.critique.model.Error
import io.critique.critique.model.User
import kotlinx.android.synthetic.main.activity_login.*

/**
 * Activity for choosing your user.
 * Also links to create a user activity.
 */
class LoginActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        // we will need it later for avatar images
        FirebaseAuth.getInstance().signInAnonymously()
    }

    /**
     * Attempts to login to the system with the given username.
     */
    fun onLogin(view: View) {
        // get the text from the EditText and trim it
        val nickname = nickname.text.toString().trim()

        if (!nickname.isNullOrBlank()) {
            // Do API call for the user
            User.getUserURL(nickname)
                    .httpGet()
                    .responseString { req, resp, result ->
                        when (result) {
                            is Result.Failure -> {
                                // got an error, show the message to the user.
                                val err = Error.fromJson(result.error.errorData)
                                toast(err.error.message)
                            }
                            is Result.Success -> {
                                val data = result.get()

                                // set our current user and switch to MainActivity
                                Globals.myUser = User.fromJson(data)
                                startActivity(Intent(this, MainActivity::class.java))
                            }
                        }
                    }
        } else {
            // Prompt it's invalid
            toast("Nickname is invalid.")
        }
    }

    /**
     * Opens the activity to create a new user.
     */
    fun onNewUser(view: View) {
        startActivityForResult(Intent(this, NewUserActivity::class.java), 1)
    }

    /**
     * To set the nickname to the EditText after a new user created.
     */
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 1 && resultCode == Activity.RESULT_OK) {
            data ?: return
            nickname.setText(data.extras.getString("nickname"))
        }
    }

    /**
     * Helper function for prompting user.
     */
    private fun toast(text: String, len: Int = Toast.LENGTH_SHORT) {
        Toast.makeText(this, text, len).show()
    }
}
