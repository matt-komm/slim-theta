install(
    FILES generateFitModel.py ModelClasses.py theta-auto.py
    DESTINATION python
    PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ
                    GROUP_EXECUTE GROUP_READ
)

install(
    DIRECTORY theta_auto
    DESTINATION python
)
