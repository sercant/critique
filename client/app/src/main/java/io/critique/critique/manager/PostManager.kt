package io.critique.critique.manager

import android.app.Activity
import android.support.v7.widget.LinearLayoutManager
import android.support.v7.widget.RecyclerView
import com.github.kittinunf.fuel.httpGet
import com.github.kittinunf.result.Result
import com.google.gson.Gson
import com.google.gson.JsonObject
import io.critique.critique.adapter.PostAdapter
import io.critique.critique.model.Post

/**
 * Manages the UI of the list with post objects
 */
class PostManager(
        private val activity: Activity,
        private val view: RecyclerView,
        private val posts: ArrayList<Post>
) {

    private var viewAdapter: RecyclerView.Adapter<*> = PostAdapter(posts)
    private var viewManager: RecyclerView.LayoutManager = LinearLayoutManager(activity)

    init {
        view.apply {
            // use this setting to improve performance if you know that changes
            // in content do not change the layout size of the RecyclerView
            setHasFixedSize(true)

            // use a linear layout manager
            layoutManager = viewManager

            // specify an viewAdapter (see also next example)
            adapter = viewAdapter
        }

        update()
    }

    /**
     * notify that the data has changed.
     */
    fun update() {
        viewAdapter.notifyDataSetChanged()
    }
}