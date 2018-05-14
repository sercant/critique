package io.critique.critique.helper

import org.apache.commons.codec.binary.Hex
import org.apache.commons.codec.digest.DigestUtils


/**
 * Helps to generate md5 for gravatar
 *
 * reference: https://fi.gravatar.com/site/implement/images/java/
 * https://stackoverflow.com/questions/9126567/method-not-found-using-digestutils-in-android
 *
 * @author  sercant
 * @date 14/05/2018
 */
object MD5Util {

    fun md5Hex(message: String): String? {
        return String(Hex.encodeHex(DigestUtils.md5(message)))
    }
}