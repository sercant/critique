package io.critique.critique.helper

import android.content.Context
import android.content.Intent
import io.critique.critique.ProfileActivity

/**
 * Helper class to parse and generate deeplinks.
 */
class DeeplinkHelper {

    companion object {
        /**
         * generating a user deeplink for application.
         *
         * @param nickname: nickname of the user
         */
        fun genUserDeeplink(nickname: String): String = "critique://users/$nickname"

        /**
         * Attempt to handle the given deeplink
         *
         * @param context: current context
         * @param link: deeplink
         */
        fun handleDeeplink(context: Context, link: String) {
            """(\w+)://(\w+)/([\w\W\d]+)""".toRegex().matchEntire(link)?.let {
                when (it.groupValues[2]) {
                    "users" -> {
                        context.startActivity(Intent(context, ProfileActivity::class.java).apply {
                            putExtra(ProfileActivity.EXTRA_NICKNAME, it.groupValues[3])
                        })
                    }
                }
            }
        }
    }
}