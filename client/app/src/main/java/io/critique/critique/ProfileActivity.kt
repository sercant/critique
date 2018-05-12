package io.critique.critique

import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.view.Menu
import android.view.MenuItem
import io.critique.critique.helper.QRCodeHelper
import io.critique.critique.manager.ProfileManager
import kotlinx.android.synthetic.main.activity_profile.*

/**
 * Profile activity for displaying user info and river posts
 */
class ProfileActivity : AppCompatActivity() {

    lateinit var profileManager: ProfileManager
    lateinit var nickname: String

    companion object {
        const val EXTRA_NICKNAME = "nickname"
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.profile_actionbar, menu)
        return super.onCreateOptionsMenu(menu)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_profile)
        setSupportActionBar(my_toolbar)

        // Get the nickname of the user from the intent extra
        if (intent.extras != null && intent.extras.containsKey(EXTRA_NICKNAME)) {
            nickname = intent.extras.getString(EXTRA_NICKNAME)
        } else {
            // if fails just close the activity
            finish()
            return
        }

        my_toolbar.title = nickname

        // instantiate the profile view manager class
        profileManager = ProfileManager(this, profile_activity, nickname)

        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.setDisplayShowHomeEnabled(true)
    }

    /**
     * navigate back to old activity
     */
    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem?): Boolean {
        when (item?.itemId) {
            R.id.user_qr_code -> {
                // Show the barcode of the user.
                QRCodeHelper.showBarcode(this, nickname)
                return true
            }
        }

        return super.onOptionsItemSelected(item)
    }
}
