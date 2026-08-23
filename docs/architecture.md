# DevKit Architecture


                User

                 |

                 ↓

          Typer CLI Layer

                 |

                 ↓

        Command Modules

(project.py, git.py, api.py)


                 |

                 ↓


          Services Layer


(project_service
 git_service
 api_service)


                 |

                 ↓


       Terminal UI Layer

(Rich Components)


                 |

                 ↓


          Operating System