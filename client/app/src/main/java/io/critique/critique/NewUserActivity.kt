package io.critique.critique

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.BitmapFactory
import android.os.Bundle
import android.provider.MediaStore
import android.support.v4.app.ActivityCompat
import android.support.v4.content.ContextCompat
import android.support.v7.app.AppCompatActivity
import android.view.View
import android.widget.EditText
import android.widget.Toast
import com.github.kittinunf.fuel.httpGet
import com.google.gson.Gson
import com.google.gson.JsonObject
import io.critique.critique.helper.FirebaseHelper
import io.critique.critique.helper.MD5Util
import io.critique.critique.model.Error
import io.critique.critique.model.User
import kotlinx.android.synthetic.main.activity_new_user.*

/**
 * Activity for creating a new user.
 */
class NewUserActivity : AppCompatActivity() {

    private val emailReg = "^[A-Za-z0-9+_.-]+@(.+)$".toRegex()
    private val birthdateReg = "\\d\\d\\d\\d-\\d\\d-\\d\\d$".toRegex()
    private var selectedPicture: String? = null

    companion object {
        const val RESULT_LOAD_IMAGE = 1
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_new_user)
        setSupportActionBar(my_toolbar)

        email.setOnFocusChangeListener { view, hasFocus ->
            if (!hasFocus) {
                val text = email.getTrimmedText()

                if (text.matches(emailReg)) {
                    tryFillGravatarProfile(text)
                }
            }
        }
    }

    /**
     * permission checking if we have the right to read images.
     */
    private fun checkPermission(): Boolean {
        return ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED
    }

    /**
     * Catches the result of the image picking.
     */
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        data ?: return

        if (requestCode == RESULT_LOAD_IMAGE && resultCode == Activity.RESULT_OK) {
            val selectedImage = data.data
            val filePathColumn = arrayOf(MediaStore.Images.Media.DATA)

            val cursor = contentResolver.query(selectedImage!!, filePathColumn, null, null, null)
            cursor!!.moveToFirst()

            val columnIndex = cursor.getColumnIndex(filePathColumn[0])
            val picturePath = cursor.getString(columnIndex)
            cursor.close()

            selectedPicture = picturePath
            user_avatar_setting.setImageBitmap(BitmapFactory.decodeFile(picturePath))
        }
    }

    /**
     * Opens up the view for selecting image from gallery
     */
    fun onChangeAvatar(view: View) {
        if (!checkPermission()) {
            // Need the permission.
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.READ_EXTERNAL_STORAGE), 2)
        } else {
            // Permission has already been granted
            pickMedia()
        }
    }

    /**
     * Catches the request permission result
     */
    override fun onRequestPermissionsResult(requestCode: Int,
                                            permissions: Array<String>, grantResults: IntArray) {
        when (requestCode) {
            2 -> {
                if ((grantResults.isNotEmpty() && grantResults.all { it == PackageManager.PERMISSION_GRANTED })) {
                    pickMedia()
                } else {
                    toast("Can't change avatar without the permissions.")
                }
            }
        }
    }

    /**
     * Opens up the view for selecting image from gallery
     */
    private fun pickMedia() {
        startActivityForResult(Intent.createChooser(Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI), "Select Picture"), RESULT_LOAD_IMAGE)
    }

    /**
     * Attempt to create a user.
     */
    fun onDone(view: View) {
        val email = email.getTrimmedText()
        if (!email.matches(emailReg)) {
            toast("Not a valid email.")
            return
        }

        val firstName = given_name.getTrimmedText()
        if (firstName.isEmpty()) {
            toast("Not a valid name.")
            return
        }

        val nickname = nickname.getTrimmedText()
        if (nickname.isEmpty()) {
            toast("Not a valid nickname.")
            return
        }

        val birthday = birthdate.getTrimmedText()
        if (!birthday.isEmpty() && !birthday.matches(birthdateReg)) {
            toast("Birthday should be in yyyy-dd-mm format.")
            return
        }

        val user = User(
                nickname = nickname,
                givenName = firstName,
                email = email,
                familyName = family_name.getTrimmedText(),
                telephone = mobile.getTrimmedText(),
                bio = bio.getTrimmedText(),
                gender = gender.getTrimmedText(),
                birthdate = birthday,
                avatar = null
        )

        selectedPicture?.let {
            FirebaseHelper.saveImageToStorage(user.getAvatarPath(), it, {

            })
            user.avatar = user.getAvatarPath()
        }

        user.createUser({
            // It was successful return back to login activity.

            setResult(Activity.RESULT_OK, Intent().apply {
                putExtra("nickname", user.nickname)
            })
            finish()
        }, {
            // Show the error.

            val error = Error.fromError(it.message, it.errorData)
            toast(error.error.message)
        })
    }

    /**
     * Trys to auto fill user information from gravatar profile
     *
     * @param email email of the user
     */
    private fun tryFillGravatarProfile(email: String) {
        val md5email = MD5Util.md5Hex(email) ?: return

        "${Globals.GRAVATAR_API_URL}/$md5email.json".httpGet()
                .responseString { _, _, result ->
                    result.fold({
                        try {
                            val profile = Gson().fromJson(it, JsonObject::class.java)
                                    .getAsJsonArray("entry")[0].asJsonObject

                            val preferredUserName = profile.get("preferredUsername").asString
                            preferredUserName?.let {
                                if (nickname.getTrimmedText().isBlank()) {
                                    nickname.setText(preferredUserName)
                                }
                            }

                            val displayName = profile.get("displayName").asString
                            displayName?.let {
                                if (given_name.getTrimmedText().isBlank()) {
                                    val names = it.split(" ")
                                    if (names.size > 1) {
                                        val lastName = names[names.size - 1]
                                        val givenName = names.subList(0, names.size - 1).joinToString(" ")

                                        given_name.setText(givenName)
                                        family_name.setText(lastName)
                                    } else {
                                        given_name.setText(it)
                                    }
                                }
                            }
                        } catch (e: Exception) {
                            //ignore
                            e.printStackTrace()
                        }

                        0
                    }, {
                        // ignore
                        it.printStackTrace()
                    })
                }
    }

    /**
     * helper function for displaying toast.
     */
    private fun toast(text: String) {
        Toast.makeText(this, text, Toast.LENGTH_SHORT).show()
    }

    /**
     * extension to edittext.
     */
    private fun EditText.getTrimmedText(): String {
        return this.text.toString().trim()
    }
}
