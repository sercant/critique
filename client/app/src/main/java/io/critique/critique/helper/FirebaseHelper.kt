package io.critique.critique.helper

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ValueEventListener
import com.google.firebase.storage.FirebaseStorage
import java.io.ByteArrayOutputStream

/**
 * Firebase helper class
 */
class FirebaseHelper {

    companion object {
        /**
         * Get the image from firebase storage
         *
         * @param path: path of the image
         * @param onSuccess: callback function
         */
        fun getImageFromStorage(path: String, onSuccess: (Bitmap?) -> Unit) {
            FirebaseStorage.getInstance().getReference(path).getBytes(1024 * 1024).addOnSuccessListener {
                onSuccess(BitmapFactory.decodeByteArray(it, 0, it.size))
            }
        }

        /**
         * Save an image to firebase storage
         *
         * @param path: path of the image
         * @param filePath: path of the image in the android device
         * @param onSuccess: callback function
         */
        fun saveImageToStorage(path: String, filePath: String, onSuccess: () -> Unit) {
            val stream = ByteArrayOutputStream()
            BitmapFactory.decodeFile(filePath).compress(Bitmap.CompressFormat.JPEG, 90, stream)
            FirebaseStorage.getInstance().getReference(path).putBytes(stream.toByteArray()).addOnSuccessListener {
                onSuccess()
            }
        }
    }
}