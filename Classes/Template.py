class Template:
    def __init__(self, type) -> None:
        self.type = type
        self.neighbors = [] # contains (type, r, α, β, γ)

# where:
# r: distance (0,0) to m_j
# α: angle m_j made from (0,0) counterclockwise
# β: angle line m_j made to the shortesh lenght to (0,0)
# γ: distance (0,0) to line m_j