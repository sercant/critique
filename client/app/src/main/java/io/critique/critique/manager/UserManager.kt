package io.critique.critique.manager

import android.app.Activity
import android.support.v7.widget.LinearLayoutManager
import android.support.v7.widget.RecyclerView
import io.critique.critique.adapter.UserAdapter
import io.critique.critique.model.User

/**
 * Manages the list type of user views
 */
class UserManager(
        private val activity: Activity,
        private val view: RecyclerView,
        private val users: ArrayList<User>
) {

    private var viewAdapter: RecyclerView.Adapter<*> = UserAdapter(users)
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
     * notify that the user list has changed.
     */
    fun update() {
        viewAdapter.notifyDataSetChanged()
    }
}