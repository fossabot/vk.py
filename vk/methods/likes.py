from .base import BaseMethod
from vk.types.responses import likes as m

import typing
from typing import Union


class Likes(BaseMethod):
    async def add(
        self,
        type: str = None,
        owner_id: int = None,
        item_id: int = None,
        access_key: str = None,
    ):
        """
        Adds the specified object to the 'Likes' list of the current user.
        :param type: Object type: 'post' — post on user or community wall, 'comment' — comment on a wall post, 'photo' — photo, 'audio' — audio, 'video' — video, 'note' — note, 'photo_comment' — comment on the photo, 'video_comment' — comment on the video, 'topic_comment' — comment in the discussion, 'sitepage' — page of the site where the [vk.com/dev/Like|Like widget] is installed
        :param owner_id: ID of the user or community that owns the object.
        :param item_id: Object ID.
        :param access_key: Access key required for an object owned by a private entity.


        """
        method = self.get_method_name(self.add)
        params = self.create_params(locals())
        r = await self.api_request(method, params)
        return m.Add(**r)

    async def delete(self, type: str = None, owner_id: int = None, item_id: int = None):
        """
        Deletes the specified object from the 'Likes' list of the current user.
        :param type: Object type: 'post' — post on user or community wall, 'comment' — comment on a wall post, 'photo' — photo, 'audio' — audio, 'video' — video, 'note' — note, 'photo_comment' — comment on the photo, 'video_comment' — comment on the video, 'topic_comment' — comment in the discussion, 'sitepage' — page of the site where the [vk.com/dev/Like|Like widget] is installed
        :param owner_id: ID of the user or community that owns the object.
        :param item_id: Object ID.


        """
        method = self.get_method_name(self.delete)
        params = self.create_params(locals())
        r = await self.api_request(method, params)
        return m.Delete(**r)

    async def get_list(
        self,
        type: str = None,
        owner_id: int = None,
        item_id: int = None,
        page_url: str = None,
        filter: str = None,
        friends_only: int = None,
        extended: bool = None,
        offset: int = None,
        count: int = None,
        skip_own: bool = None,
    ):
        """
        Returns a list of IDs of users who added the specified object to their 'Likes' list.
        :param type: , Object type: 'post' — post on user or community wall, 'comment' — comment on a wall post, 'photo' — photo, 'audio' — audio, 'video' — video, 'note' — note, 'photo_comment' — comment on the photo, 'video_comment' — comment on the video, 'topic_comment' — comment in the discussion, 'sitepage' — page of the site where the [vk.com/dev/Like|Like widget] is installed
        :param owner_id: ID of the user, community, or application that owns the object. If the 'type' parameter is set as 'sitepage', the application ID is passed as 'owner_id'. Use negative value for a community id. If the 'type' parameter is not set, the 'owner_id' is assumed to be either the current user or the same application ID as if the 'type' parameter was set to 'sitepage'.
        :param item_id: Object ID. If 'type' is set as 'sitepage', 'item_id' can include the 'page_id' parameter value used during initialization of the [vk.com/dev/Like|Like widget].
        :param page_url: URL of the page where the [vk.com/dev/Like|Like widget] is installed. Used instead of the 'item_id' parameter.
        :param filter: Filters to apply: 'likes' — returns information about all users who liked the object (default), 'copies' — returns information only about users who told their friends about the object
        :param friends_only: Specifies which users are returned: '1' — to return only the current user's friends, '0' — to return all users (default)
        :param extended: Specifies whether extended information will be returned. '1' — to return extended information about users and communities from the 'Likes' list, '0' — to return no additional information (default)
        :param offset: Offset needed to select a specific subset of users.
        :param count: Number of user IDs to return (maximum '1000'). Default is '100' if 'friends_only' is set to '0', otherwise, the default is '10' if 'friends_only' is set to '1'.
        :param skip_own:


        """
        method = self.get_method_name(self.get_list)
        params = self.create_params(locals())
        r = await self.api_request(method, params)
        return m.GetList(**r)

    async def is_liked(
        self,
        user_id: int = None,
        type: str = None,
        owner_id: int = None,
        item_id: int = None,
    ):
        """
        Checks for the object in the 'Likes' list of the specified user.
        :param user_id: User ID.
        :param type: Object type: 'post' — post on user or community wall, 'comment' — comment on a wall post, 'photo' — photo, 'audio' — audio, 'video' — video, 'note' — note, 'photo_comment' — comment on the photo, 'video_comment' — comment on the video, 'topic_comment' — comment in the discussion
        :param owner_id: ID of the user or community that owns the object.
        :param item_id: Object ID.


        """
        method = self.get_method_name(self.is_liked)
        params = self.create_params(locals())
        r = await self.api_request(method, params)
        return m.IsLiked(**r)
