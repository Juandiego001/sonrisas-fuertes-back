from http.client import HTTPException
from apiflask import APIBlueprint, abort
from app.schemas.profile import ProfileIn, ProfileOut, Profiles
from app.schemas.generic import Message
from app.services import profile


bp = APIBlueprint('profile', __name__)


@bp.post('/')
@bp.input(ProfileIn)
@bp.output(Message)
def create_profile(data):
    try:
        profile.create_profile(data)
        return {'message': 'Profile created successfully'}
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/')
@bp.output(Profiles)
def get_profiles():
    try:
        profiles = Profiles().dump({'items': profile.get_profiles()})
        return profiles
    except Exception as ex:
        abort(500, str(ex))


@bp.get('/<string:profileid>')
@bp.output(ProfileOut)
def get_profile_detail(profileid):
    try:
        return profile.get_profile_detail(profileid)
    except HTTPException as ex:
        abort(401, ex.description)
    except Exception as e:
        raise HTTPException(500, e)


@bp.patch('/<string:profileid>')
@bp.input(ProfileIn)
@bp.output(Message)
def update_profile(profileid, data):
    try:
        profile.update_profile(profileid, data)
        return {'message': 'Profile updated successfully'}
    except Exception as ex:
        abort(500, str(ex))
