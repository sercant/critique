package io.critique.critique

import android.Manifest.permission.READ_EXTERNAL_STORAGE
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
import io.critique.critique.helper.FirebaseHelper
import io.critique.critique.model.Error
import kotlinx.android.synthetic.main.activity_edit_profile.*

/**
 * Edit profile activity
 */
class EditProfileActivity : AppCompatActivity() {

    private val birthdateReg = "\\d\\d\\d\\d-\\d\\d-\\d\\d$".toRegex()
    private var selectedPicture: String? = null

    companion object {
        const val RESULT_LOAD_IMAGE = 1
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_edit_profile)
        setSupportActionBar(my_toolbar)

        val user = Globals.myUser

        // pre fill the fields
        user.apply {
            name_text.setText(givenName)
            family_name_text.setText(familyName)
            bio_text.setText(bio)
            mobile_text.setText(telephone)
            gender_text.setText(gender)
            birthdate_text.setText(birthdate)
            avatar?.let {
                FirebaseHelper.getImageFromStorage(it, {
                    it ?: return@getImageFromStorage

                    user_avatar_setting.setImageBitmap(it)
                })
            }
        }

        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.setDisplayShowHomeEnabled(true)
    }

    /**
     * Go back to the other activity.
     */
    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }

    /**
     * check if we have required permissions
     */
    private fun checkPermission(): Boolean {
        return ContextCompat.checkSelfPermission(this, READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED
    }

    /**
     * Attempt to save the user.
     */
    fun onDone(view: View) {
        val firstName = name_text.getTrimmedText()
        if (firstName.isEmpty()) {
            toast("Not a valid name.")
            return
        }

        val birthday = birthdate_text.getTrimmedText()
        if (!birthday.isEmpty() && !birthday.matches(birthdateReg)) {
            toast("Birthday should be in yyyy-mm-dd format.")
            return
        }

        val user = Globals.myUser.copy(
                givenName = firstName,
                familyName = family_name_text.getTrimmedText(),
                telephone = mobile_text.getTrimmedText(),
                bio = bio_text.getTrimmedText(),
                gender = gender_text.getTrimmedText(),
                birthdate = birthday)

        selectedPicture?.let {
            FirebaseHelper.saveImageToStorage(user.getAvatarPath(), it, {

            })
            user.avatar = user.getAvatarPath()
        }

        Globals.myUser.updateUser(user, {
            finish()
        }, {
            val err = Error.fromError(it?.message, it?.errorData)
            toast(err.error.message)
        })
    }

    /**
     * user clicked change avatar. check permissions
     */
    fun onChangeAvatar(view: View) {
        // Here, thisActivity is the current activity
        if (!checkPermission()) {
            // No explanation needed, we can request the permission.
            ActivityCompat.requestPermissions(this, arrayOf(READ_EXTERNAL_STORAGE), 2)

        } else {
            // Permission has already been granted
            pickMedia()
        }
    }

    /**
     * Retrieve the information of the image selection
     */
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode == RESULT_LOAD_IMAGE && resultCode == Activity.RESULT_OK && data != null) {
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
     * check whether the permissions granted or not
     */
    override fun onRequestPermissionsResult(requestCode: Int,
                                            permissions: Array<String>, grantResults: IntArray) {
        when (requestCode) {
            2 -> {
                if ((grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED)) {
                    // Permission has already been granted
                    pickMedia()
                } else {
                    toast("We need this permission to change your avatar.")
                }
                return
            }
        }
    }

    /**
     * start activity to pick image
     */
    private fun pickMedia() {
        startActivityForResult(Intent.createChooser(Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI), "Select Picture"), RESULT_LOAD_IMAGE)
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
