package io.critique.critique

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.Bundle
import android.support.design.widget.BottomNavigationView
import android.support.v7.app.AppCompatActivity
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.Toast
import com.github.kittinunf.fuel.httpGet
import com.google.gson.Gson
import com.google.gson.JsonObject
import com.google.zxing.integration.android.IntentIntegrator
import io.critique.critique.helper.DeeplinkHelper
import io.critique.critique.helper.QRCodeHelper
import io.critique.critique.manager.PostManager
import io.critique.critique.manager.ProfileManager
import io.critique.critique.manager.UserManager
import kotlinx.android.synthetic.main.activity_main.*

/**
 * Main page of the application. Has 3 tabs,
 *
 * First tab is a list of users in the system.
 * Second tab is the list of posts that user has in his/her inbox.
 * Third tab is the profile of the current user.
 */
class MainActivity : AppCompatActivity() {

    companion object {
        const val EXTRA_SHOW_WEATHER = "extra_show_weather"
    }

    // View managers
    lateinit var userManager: UserManager
    lateinit var inboxManager: PostManager
    lateinit var profileManager: ProfileManager

    // receiver to handle some events
    private val broadcastReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            intent ?: return

            when (intent.action) {
                Events.ACTION_POST_DELETE, Events.ACTION_POST_PUBLISH -> {
                    Globals.myUser.queryRiver {
                        profileManager.update()
                    }

                    Globals.myUser.queryInbox {
                        inboxManager.update()
                    }
                }
            }
        }

    }

    /**
     * Inflates different kinds of toolbars for the tabs
     */
    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        when (navigation.selectedItemId) {
            R.id.navigation_users -> {
                menuInflater.inflate(R.menu.feed_actionbar, menu)
            }
            R.id.navigation_inbox -> {
                menuInflater.inflate(R.menu.inbox_actionbar, menu)
            }
            R.id.navigation_profile -> {
                menuInflater.inflate(R.menu.my_profile_actionbar, menu)
            }
        }
        return super.onCreateOptionsMenu(menu)
    }

    /**
     * Handle toolbar menu clicks
     */
    override fun onOptionsItemSelected(item: MenuItem?): Boolean {
        when (item?.itemId) {
            R.id.user_qr_code -> {
                QRCodeHelper.showBarcode(this, Globals.myUser.nickname)
                return true
            }
            R.id.edit_profile -> {
                startActivity(Intent(this, EditProfileActivity::class.java))

                return true
            }
            R.id.search_user -> {
                IntentIntegrator(this).initiateScan()
                return true
            }
        }
        return super.onOptionsItemSelected(item)
    }

    /**
     * Listener for tab changes
     */
    private val mOnNavigationItemSelectedListener = BottomNavigationView.OnNavigationItemSelectedListener { item ->
        when (item.itemId) {
            R.id.navigation_users -> {
                switchToHome()
                return@OnNavigationItemSelectedListener true
            }
            R.id.navigation_inbox -> {
                switchToInbox()
                return@OnNavigationItemSelectedListener true
            }
            R.id.navigation_profile -> {
                switchToProfile()
                return@OnNavigationItemSelectedListener true
            }
        }
        false
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setSupportActionBar(my_toolbar)

        navigation.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener)

        // query all users for listing them
        Globals.queryUsers {
            userManager = UserManager(this, users_tab, it)
        }

        // query user inbox for listing on the second tab
        Globals.myUser.queryInbox {
            inboxManager = PostManager(this, inbox_tab, it)
        }

        // setup the profile manager for the third tab
        profileManager = ProfileManager(this, profile_tab, Globals.myUser.nickname)

        when (navigation.selectedItemId) {
            R.id.navigation_users -> {
                switchToHome()

            }
            R.id.navigation_inbox -> {
                switchToInbox()
            }
            R.id.navigation_profile -> {
                switchToProfile()
            }
        }

        registerReceiver(broadcastReceiver, IntentFilter().apply {
            addAction(Events.ACTION_POST_PUBLISH)
            addAction(Events.ACTION_POST_DELETE)
        })

        // should I show the weather info?
        if (intent.extras?.getBoolean(EXTRA_SHOW_WEATHER) == true) {
            val currentCity = "Oulu"
            "${Globals.WEATHER_API_URL}/weather?appid=${Globals.WEATHER_API_KEY}&q=$currentCity&units=metric"
                    .httpGet()
                    .responseString { _, _, result ->
                        result.fold({
                            val weatherData = Gson().fromJson(it, JsonObject::class.java)

                            try {
                                // form the weather information string.
                                var weatherText = ""
                                val description = weatherData.getAsJsonArray("weather")[0]
                                        .asJsonObject.get("description").asString
                                val temperature = weatherData.getAsJsonObject("main")
                                        .get("temp").asDouble

                                weatherText += "Welcome ${Globals.myUser.nickname}!\n"
                                weatherText += "Weather is $description\n"
                                weatherText += "Temperature is $temperature degrees"

                                // Show it as a toast message.
                                Toast.makeText(this, weatherText, Toast.LENGTH_LONG).show()
                            } catch (e: Exception) {
                                // ignore
                                e.printStackTrace()
                            }
                        }, {
                            // ignore
                            it.printStackTrace()
                        })
                    }
            intent.removeExtra(EXTRA_SHOW_WEATHER)
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        unregisterReceiver(broadcastReceiver)
    }

    /**
     * capture the barcode reader result
     */
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        val result = IntentIntegrator.parseActivityResult(requestCode, resultCode, data)
        if (result != null) {
            if (result.contents != null) {
                DeeplinkHelper.handleDeeplink(this, result.contents)
            }
        } else {
            super.onActivityResult(requestCode, resultCode, data)
        }
    }

    /**
     * change view to home
     */
    private fun switchToHome() {
        title = "Users"
        profile_tab.visibility = View.GONE
        users_tab.visibility = View.VISIBLE
        inbox_tab.visibility = View.GONE
        invalidateOptionsMenu()
    }

    /**
     * change view to inbox
     */
    private fun switchToInbox() {
        title = "Inbox"
        profile_tab.visibility = View.GONE
        users_tab.visibility = View.GONE
        inbox_tab.visibility = View.VISIBLE
        invalidateOptionsMenu()
    }

    /**
     * change view to profile
     */
    private fun switchToProfile() {
        title = profileManager.user?.nickname ?: "Profile"
        profile_tab.visibility = View.VISIBLE
        users_tab.visibility = View.GONE
        inbox_tab.visibility = View.GONE
        invalidateOptionsMenu()
    }
}
