void RegisterSystem<TSystem>(TSystem system) where TSystem : ISystem
{
    system.SetArchitecture(this);
    mContainer.Register<TSystem>(system);

    if (!mInited)
    {
        mSystems.Add(system);
    }
    else
    {
        system.Init();
    }
}