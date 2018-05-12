package io.critique.critique.helper

import android.app.Dialog
import android.content.Context
import android.graphics.Color
import android.graphics.drawable.ColorDrawable
import android.view.ViewGroup
import android.view.Window
import android.widget.ImageView
import android.widget.RelativeLayout
import com.google.zxing.BarcodeFormat
import com.journeyapps.barcodescanner.BarcodeEncoder
import io.critique.critique.Globals

/**
 * QR code helper function.
 */
class QRCodeHelper {
    companion object {

        /**
         * Show barcode of the user
         *
         * @param context: current context
         * @param nickname: nickname of the user.
         */
        fun showBarcode(context: Context, nickname: String) {
            try {
                val barcodeEncoder = BarcodeEncoder()
                val bitmap = barcodeEncoder.encodeBitmap(DeeplinkHelper.genUserDeeplink(nickname), BarcodeFormat.QR_CODE, 500, 500)

                val imageView = ImageView(context)
                imageView.setImageBitmap(bitmap)

                Dialog(context).apply {
                    requestWindowFeature(Window.FEATURE_NO_TITLE)
                    window.setBackgroundDrawable(ColorDrawable(Color.TRANSPARENT))
                    setOnDismissListener {  }
                    addContentView(imageView, RelativeLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT))
                }.show()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}